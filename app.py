from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session
from ultralytics import YOLO
import cv2, os, time, datetime, uuid, torch, random, smtplib, json
from email.mime.text import MIMEText
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "shield_ai_ultra_secret"

app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit for uploads

# ================== 🔥 MODEL ==================
device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("best.pt").to(device)

# ================== 📁 SETUP ==================
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

VIOLATION_FOLDER = os.path.join("static", "violations")
os.makedirs(VIOLATION_FOLDER, exist_ok=True)

ADMIN_USER = "admin"
PASSWORD_FILE = "password.json"

# ================== 📧 EMAIL ==================
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# ================== 🔐 RESET DATA ==================
reset_data = {
    "otp": None,
    "user": None,
    "email": None,
    "expiry": None
}

# ================== 📊 STATS ==================
stats = {
    "frames": 0,
    "violations": 0,
    "safe": 0,
    "start_time": time.time(),
    "fps": 0,
    "violation_history": [] 
}

counted_ids = set()

def reset_stats():
    global counted_ids
    counted_ids = set() # Clear the unique IDs on reset
    stats.update({
        "frames": 0,
        "violations": 0,
        "safe": 0,
        "start_time": time.time(),
        "fps": 0,
        "violation_history": []
    })

# ================== 🔑 PASSWORD DATASET ==================
def get_admin_pass():
    if not os.path.exists(PASSWORD_FILE):
        return "1234"
    with open(PASSWORD_FILE, "r") as f:
        data = json.load(f)
    return data.get("admin", {}).get("password", "1234")

def set_admin_pass(new_pass):
    data = {"admin": {"password": new_pass}}
    with open(PASSWORD_FILE, "w") as f:
        json.dump(data, f)

# ================== ✉️ EMAIL OTP ==================
def send_otp_email(to_email, otp):
    subject = "SHIELD-AI Password Reset OTP"
    body = f"Your OTP is: {otp}\nValid for 5 minutes."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email failed:", e)

# ================== ⚡ PROCESS FRAME ==================
def process_frame(frame):
    results = model(frame, conf=0.3, imgsz=320, iou=0.5, verbose=False)[0]
    v_count, s_count = 0, 0

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if cls == 1:
            label, color = f"NO HELMET {conf:.2f}", (0, 0, 255)
            v_count += 1
            # This ensures each violation is logged in the trend
            stats["violation_history"].append(time.time())
        else:
            label, color = f"HELMET {conf:.2f}", (0, 255, 0)
            s_count += 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame, v_count, s_count

# ================== 🔐 LOGIN ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        if username == ADMIN_USER and password == get_admin_pass():
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================== 🔑 FORGOT PASSWORD ==================
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        if username == ADMIN_USER:
            otp = str(random.randint(1000, 9999))
            reset_data["otp"] = otp
            reset_data["user"] = username
            reset_data["email"] = email
            reset_data["expiry"] = time.time() + 300
            print("🔥 OTP (Terminal Backup):", otp)
            send_otp_email(email, otp)
            return render_template("verify_otp.html")
        else:
            return render_template("forgot.html", error="User not found")
    return render_template("forgot.html")

# ================== 🔐 VERIFY OTP ==================
@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    user_otp = request.form.get("otp")
    if time.time() > reset_data["expiry"]:
        return render_template("verify_otp.html", error="OTP Expired")
    if user_otp == reset_data["otp"]:
        return render_template("reset_password.html")
    else:
        return render_template("verify_otp.html", error="Invalid OTP")

# ================== 🔁 RESET PASSWORD ==================
@app.route("/reset_password", methods=["POST"])
def reset_password():
    new_pass = request.form.get("password").strip()
    confirm_pass = request.form.get("confirm").strip()
    if new_pass != confirm_pass:
        return render_template("reset_password.html", error="Passwords do not match")
    set_admin_pass(new_pass)
    reset_data["otp"] = None
    return redirect(url_for("login"))

# ================== 🏠 HOME ==================
@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

# ================== 🖼 IMAGE PREDICTION ==================
@app.route("/predict", methods=["POST"])
def predict():
    reset_stats()
    file = request.files["file"]
    filename = f"{uuid.uuid4()}.jpg"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    img = cv2.imread(path)
    img = cv2.resize(img, (640, 360))
    
    processed, v, s = process_frame(img)
    
    stats["violations"] = v
    stats["safe"] = s
    stats["fps"] = 1  # Since it's a single image, we can set FPS to 1 for display purposes
    
    out_path = os.path.join(UPLOAD_FOLDER, "proc_" + filename)
    cv2.imwrite(out_path, processed)
    return jsonify({"image": url_for('static', filename='uploads/proc_' + filename)})

# ================== 🎥 VIDEO FEED ==================
def video_generator(video_path, frame_skip=3):
    cap = cv2.VideoCapture(video_path)
    frame_id = 0
    last_annotated_frame = None 
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.resize(frame, (640, 360))
        frame_id += 1
        
        if frame_id % frame_skip == 0:
            results = model.track(frame, persist=True, conf=0.3, imgsz=640, iou=0.5, verbose=False)[0]
            
            if results.boxes.id is not None:
                ids = results.boxes.id.int().cpu().tolist()
                clss = results.boxes.cls.int().cpu().tolist()
                boxes = results.boxes.xyxy.int().cpu().tolist()
                confs = results.boxes.conf.float().cpu().tolist()

                for box, obj_id, cls, conf in zip(boxes, ids, clss, confs):
                    is_violation = (cls == 1)
                    color = (0, 0, 255) if is_violation else (0, 255, 0)
                    label = f"ID:{obj_id} {'NO HELMET' if is_violation else 'HELMET'}"
                    
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
                    cv2.putText(frame, label, (box[0], box[1] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    if obj_id not in counted_ids:
                        counted_ids.add(obj_id)
                        if is_violation:
                            stats["violations"] += 1
                            # For Live Analytics Trend
                            stats["violation_history"].append(time.time())

                            # --- SEVERITY LOGIC ---
                            # We check how many 'NO HELMET' detections are in the current results
                            current_violations = len([b for b in results.boxes if int(b.cls[0]) == 1])                            
                            if current_violations >= 2:
                                severity = "HIGH"    # Multiple people/Triple riding without helmets
                            else:
                                severity = "MEDIUM"  # Single rider without helmet

                            # 📸 EVIDENCE CAPTURE LOGIC 
                            try:
                                h, w, _ = frame.shape
                                x1, y1, x2, y2 = box
                                x1, y1 = max(0, x1), max(0, y1)
                                x2, y2 = min(w, x2), min(h, y2)

                                padding_x = 80  
                                padding_y = 100 

                                px1 = max(0, x1 - padding_x)
                                py1 = max(0, y1 - padding_y)
                                px2 = min(w, x2 + padding_x)
                                py2 = min(h, y2 + padding_y)

                                crop = frame[py1:py2, px1:px2]
                                timestamp = time.strftime("%Y%m%d-%H%M%S")
                                
                                crop_filename = f"{severity}_ID{obj_id}_{timestamp}.jpg"
                                crop_path = os.path.join(VIOLATION_FOLDER, crop_filename)
                                cv2.imwrite(crop_path, crop)
                            except Exception as e:
                                print(f"❌ Failed to save crop: {e}")
                        else: stats["safe"] += 1
            last_annotated_frame = frame.copy()
        
        display_frame = last_annotated_frame if last_annotated_frame is not None else frame

        stats["frames"] += 1
        dt = time.time() - stats["start_time"]
        if dt > 0: stats["fps"] = round(stats["frames"] / dt, 2)
            
        _, img = cv2.imencode('.jpg', display_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + img.tobytes() + b'\r\n')
        
    cap.release()

@app.route("/video_feed")
def video_feed():
    video_path = session.get("video_path")
    if not video_path:
        return "No video uploaded"
    return Response(video_generator(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/get_violations")
def get_violations():
    try:
        files = os.listdir(VIOLATION_FOLDER)
        files = [f for f in files if f.endswith('.jpg')]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(VIOLATION_FOLDER, x)), reverse=True)
        recent_files = [url_for('static', filename='violations/' + f) for f in files[:2]]
        return jsonify(recent_files)
    except Exception as e:
        return jsonify([])

@app.route("/gallery")
def gallery():
    images = []
    if os.path.exists(VIOLATION_FOLDER):
        for filename in os.listdir(VIOLATION_FOLDER):
            if filename.endswith(".jpg"):
                # Determine severity by checking the filename prefix
                severity = "High" if filename.startswith("HIGH") else "Medium"
                
                path = os.path.join(VIOLATION_FOLDER, filename)
                ctime = os.path.getctime(path)
                date_str = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')

                images.append({
                    "url": url_for('static', filename='violations/' + filename),
                    "date": date_str,
                    "type": "No Helmet",
                    "severity": severity
                })
    # Sort by newest first
    images.sort(key=lambda x: x['date'], reverse=True)
    return render_template("gallery.html", images=images)

@app.route("/webcam_feed")
def webcam_feed():
    def gen():
        cap = cv2.VideoCapture(0)
        frame_skip = 2
        frame_id = 0
        while True:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.resize(frame, (640, 360))
            frame_id += 1
            if frame_id % frame_skip == 0:
                proc, v, s = process_frame(frame)
                stats["violations"] = v
                stats["safe"] = s
            else: proc = frame
            stats["frames"] += 1
            dt = time.time() - stats["start_time"]
            if dt > 0: stats["fps"] = round(stats["frames"] / dt, 2)
            _, img = cv2.imencode('.jpg', proc, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + img.tobytes() + b'\r\n')
        cap.release()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/upload_video", methods=["POST"])
def upload_video():
    reset_stats()
    file = request.files["video"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    session["video_path"] = path
    return jsonify({"status": "ok"})

# ================== 📊 STATS FOR CHART ==================
@app.route("/stats")
def get_stats():
    # Calculate violations in the last 60 seconds
    now = time.time()
    v_last_min = len([t for t in stats["violation_history"] if now - t < 60])
    
    # Return original stats + the new trend data
    return jsonify({
        "frames": stats["frames"],
        "violations": stats["violations"],
        "safe": stats["safe"],
        "fps": stats["fps"],
        "v_per_minute": v_last_min
    })

from fpdf import FPDF
import datetime

@app.route("/generate_report")
def generate_report():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    # 1. Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # 2. Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(59, 130, 246) # Shield-AI Blue
    pdf.cell(0, 10, "SHIELD-AI TRAFFIC VIOLATION REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)

    # 3. Summary Section
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "  Summary Statistics", ln=True, fill=True)
    pdf.set_font("Arial", '', 12)
    
    all_files = [f for f in os.listdir(VIOLATION_FOLDER) if f.endswith('.jpg')]
    high_sev = len([f for f in all_files if f.startswith("HIGH")])
    
    pdf.cell(0, 8, f"Total Violations Recorded: {len(all_files)}", ln=True)
    pdf.cell(0, 8, f"High Severity Incidents: {high_sev}", ln=True)
    pdf.cell(0, 8, f"Safe Riders Detected: {stats['safe']}", ln=True)
    pdf.ln(10)

    # 4. Detailed Evidence List
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "  Evidence Logs", ln=True, fill=True)
    pdf.ln(5)

    # Loop through images and add to PDF
    # We take the 10 most recent to keep the file size manageable
    all_files.sort(key=lambda x: os.path.getmtime(os.path.join(VIOLATION_FOLDER, x)), reverse=True)
    
    for filename in all_files[:10]:
        path = os.path.join(VIOLATION_FOLDER, filename)
        timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
        sev = "High" if filename.startswith("HIGH") else "Medium"
        
        # Add Text Description
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, f"ID: {filename.split('_')[1]} | Severity: {sev} | Time: {timestamp}", ln=True)
        
        # Add the Evidence Image
        # Image(path, x, y, width, height)
        pdf.image(path, w=100)
        pdf.ln(5)

    # 5. Output
    report_name = f"Violation_Report_{datetime.date.today()}.pdf"
    pdf.output(report_name)
    
    # Send file to user for download
    from flask import send_file
    return send_file(report_name, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)