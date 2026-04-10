# **🛡️ SHIELD-AI: Helmet Detection for Two-Wheeler Riders**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-AI%20Model-red.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)
![Status](https://img.shields.io/badge/Project-Active-brightgreen.svg)

---

## 🚀 Overview

**SHIELD-AI** is an AI-powered traffic safety system that detects whether two-wheeler riders are wearing helmets using **YOLOv8**.

It supports:
- 📸 Image detection  
- 🎥 Video analysis  
- 📷 Live webcam monitoring  
- 📊 Analytics dashboard  
- 🚨 Violation tracking & reporting  

---

## ✨ Features

- ✅ Helmet vs No-Helmet Detection (YOLOv8)
- 🎥 Real-time Webcam Monitoring
- 📁 Video & Image Upload Processing
- ⚡ Live FPS & Performance Tracking
- 🚨 Automatic Violation Detection
- 📸 Evidence Capture System
- 📊 Analytics Dashboard (Charts)
- 🖼 Evidence Gallery
- 📄 PDF Report Generation
- 🔐 Admin Login with OTP Reset
- 📧 Email Notification System

---

## 🧠 Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Flask (Python) |
| AI Model | YOLOv8 (Ultralytics) |
| Frontend | HTML, CSS, JavaScript |
| Visualization | Chart.js |
| Image Processing | OpenCV |
| Authentication | Flask Sessions |
| Reports | FPDF |
| Email Service | SMTP (Gmail) |

---

## 📂 Project Structure
```
Helmet-Detection_For_Two-wheeler/
│
├── static/
│   ├── uploads/          # Uploaded media
│   ├── violations/       # Captured evidence
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── gallery.html
│
├── app.py                # Main Flask app
├── best.pt               # YOLOv8 trained model
├── password.json         # Admin credentials
├── requirements.txt
├── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```
git clone https://github.com/Jiyapatel2107/Helmet-Detection_For_Two-wheeler-
cd Helmet-Detection_For_Two-wheeler
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)
```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

If requirements.txt not available, install manually:
```
pip install flask ultralytics opencv-python torch fpdf
```

### ▶️ Run the Application
```
python app.py
```
Then open in browser:
```
http://127.0.0.1:5000
```
---

## 🔐 Default Login

- Username: admin
- Password: 1234

 (You can reset password using OTP system)

 ---

## 📸 How It Works

**🔹 Image Detection**
- Upload an image
- System detects helmet / no-helmet
- Displays annotated output

**🔹 Video Detection**
- Upload video
- Processes frames using YOLO tracking
- Counts unique violations

**🔹 Live Webcam**
- Real-time detection
- Continuous monitoring

---

## 🚨 Violation System
- Detects No Helmet Riders
- Assigns severity:
  - 🟡 Medium → Single violation
  - 🔴 High → Multiple riders / severe case
- Automatically captures:
  - Cropped evidence image
  - Timestamp
  - Saved in:  "/static/violations "
---

## 📊 Analytics Dashboard
- 📈 Violations per minute (Line Chart)
- 🥧 Safe vs Unsafe ratio (Pie Chart)
- ⚡ FPS tracking
- 📋 Real-time activity logs
---

## 🖼 Evidence Gallery
Displays:
- Captured violation images
- Timestamp
- Severity level
- Detection results
---

## 📄 Report Generation
- Generate Daily PDF Report
- Includes:
    - Total violations
    - Severity breakdown
    - Evidence images
---

## 📧 Email OTP System
- Used for password reset
- Requires environment variables:
```
set EMAIL_USER=your_email@gmail.com
set EMAIL_PASS=your_app_password
```
---

## 🧪 Model Info
- Model: YOLOv8 Custom Trained
- Classes:
    - Helmet ✅
    - No Helmet ❌
---

## 🔥 Future Improvements
- 🚀 Deploy on cloud (AWS / Render)
- 📱 Mobile App Integration
- 🚓 Auto challan system
- 📡 CCTV Integration
- 🧾 License plate recognition
---

## 🙌 Acknowledgements
- Ultralytics YOLOv8
- OpenCV
- Flask Community
---

## 👨‍💻 Developer

**Jiya Patel**

📧 Email: jiya2172005@gmail.com

🔗 GitHub: https://github.com/Jiyapatel2107

---

## ⭐ If you like this project

- ⭐ Star the repository
- 🍴 Fork it
- 🚀 Share it with others
