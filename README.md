🛡️ SHIELD-AI: Helmet Detection for Two-Wheeler Riders

🚀 SHIELD-AI is an AI-powered traffic safety system that detects whether two-wheeler riders are wearing helmets using YOLOv8. It supports real-time monitoring via image, video, and live webcam, and provides analytics, violation tracking, and automated reporting.

📌 Features

✅ Helmet vs No-Helmet Detection (YOLOv8)
✅ Real-time Webcam Monitoring
✅ Video Upload & Analysis
✅ Image Detection
✅ Live FPS & Performance Tracking
✅ Violation Detection with Evidence Capture
✅ Activity Logs & Alerts
✅ Analytics Dashboard (Charts & Stats)
✅ Evidence Gallery (Captured Violations)
✅ PDF Report Generation
✅ Admin Login System with OTP Reset

🧠 Tech Stack
Category	Technology Used
Backend	Flask (Python)
AI Model	YOLOv8 (Ultralytics)
Frontend	HTML, CSS, JavaScript
Visualization	Chart.js
Image Processing	OpenCV
Authentication	Flask Session
Report Generation	FPDF
Email Service	SMTP (Gmail)
📂 Project Structure
SHIELD-AI/
│
├── static/
│   ├── uploads/          # Uploaded & processed images/videos
│   ├── violations/       # Captured violation evidence
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── gallery.html
│
├── app.py                # Main Flask Application
├── best.pt               # YOLO trained model
├── password.json         # Admin password storage
├── README.md
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/Helmet-Detection_For_Two-wheeler.git
cd Helmet-Detection_For_Two-wheeler
2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
If requirements.txt not available, install manually:
pip install flask ultralytics opencv-python torch fpdf
▶️ Run the Application
python app.py
Then open in browser:
http://127.0.0.1:5000
🔐 Default Login
Username: admin
Password: 1234
(You can reset password using OTP system)
📸 How It Works
🔹 Image Detection
Upload an image
System detects helmet / no-helmet
Displays annotated output
🔹 Video Detection
Upload video
Processes frames using YOLO tracking
Counts unique violations
🔹 Live Webcam
Real-time detection
Continuous monitoring
🚨 Violation System
Detects No Helmet Riders
Assigns severity:
🟡 Medium → Single violation
🔴 High → Multiple riders / severe case
Automatically captures:
Cropped evidence image
Timestamp
Stored in /static/violations
📊 Analytics Dashboard
📈 Violations per minute (Line Chart)
🥧 Safe vs Unsafe ratio (Pie Chart)
⚡ FPS tracking
📋 Real-time activity logs
🖼 Evidence Gallery
View all captured violations
Includes:
Image
Date & Time
Severity Level
📄 Report Generation
Generate Daily PDF Report
Includes:
Total violations
Severity breakdown
Evidence images
📧 Email OTP System
Used for password reset
Requires environment variables:
set EMAIL_USER=your_email@gmail.com
set EMAIL_PASS=your_app_password
🧪 Model Info
Model: YOLOv8 Custom Trained
Classes:
Helmet ✅
No Helmet ❌
🔥 Future Improvements
🚀 Deploy on cloud (AWS / Render)
📱 Mobile App Integration
🚓 Auto challan system
📡 CCTV Integration
🧾 License plate recognition
🙌 Acknowledgements
Ultralytics YOLOv8
OpenCV
Flask Community
📬 Contact

👤 Your Name
📧 your-email@example.com

🔗 GitHub: https://github.com/your-username

⭐ If you like this project

Give it a ⭐ on GitHub and share it!
