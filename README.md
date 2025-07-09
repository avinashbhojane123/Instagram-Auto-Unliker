# 📸 Instagram Auto Unliker

A full-stack tool built using **React.js (Frontend)** and **Flask + Instagrapi (Backend)** to automatically unlike previously liked Instagram posts in bulk with a user-friendly interface.

---

## 🚀 Features

- ✅ Auto login with Instagram credentials
- 🔄 Automatically fetch and unlike up to 3000 posts
- 🕒 Re-check interval and unlike delay configuration
- 🔢 Live counter showing number of posts unliked
- 📜 Real-time logs displayed in the UI
- 🌗 Light/Dark Mode toggle
- 🔔 Toast notifications for success and error states
- ⚛️ Built with modern technologies

---

## 🛠 Tech Stack

| Layer     | Technology         |
|-----------|--------------------|
| Frontend  | React.js, Toastify |
| Backend   | Flask, instagrapi  |
| UI        | Custom CSS         |
| CORS      | Enabled (Flask-CORS) |

---

## 📦 Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/avinashbhojane123/Instagram-Auto-Unliker.git
cd Instagram-Auto-Unliker

2. Setup the Backend
cd backend
pip install -r requirements.txt
python app.py

2. Setup the Frontend
cd ../frontend
npm install
npm start
Visit: http://localhost:3000


📁 Folder Structure
Instagram-Auto-Unliker/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.js
│   └── package.json
└── README.md

🧪 How It Works
Logs into your account using instagrapi

Fetches your liked media (/feed/liked)

Iteratively unlikes all items with delays

Repeats the process on a schedule until stopped

Displays real-time logs and stats via API


⚠ Disclaimer
This project is created for educational purposes only.
Use it at your own risk.
The developer is not responsible for any misuse or violation of Instagram’s terms of service.
Avoid excessive usage to prevent account rate-limiting or bans.

📄 License
MIT License © 2025 Avinash Bhojane

