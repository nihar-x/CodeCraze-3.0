# 🚗 ParkMate: Smart Parking Management System

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

![ParkMate Banner](./docs/images/banner.png)

ParkMate is a modern, full-stack parking management solution designed to streamline the experience of finding and booking parking slots. With a premium SaaS-inspired dashboard, real-time availability tracking, and a robust admin panel, ParkMate bridges the gap between parking providers and users.

---

## ✨ Key Features

### 👤 For Users
- **Real-time Availability:** Check empty slots instantly before visiting.
- **Easy Booking:** Secure your spot with a few clicks.
- **Secure Authentication:** OTP-based login and signup for enhanced security.
- **Booking History:** Keep track of all your past and upcoming reservations.
- **Payment Integration:** Seamless mock payment flow for a complete experience.

### 🛡️ For Admins
- **Inventory Management:** Add, remove, or update parking slots easily.
- **Live Monitoring:** View all active bookings and occupancy rates.
- **User Management:** Oversee user activities and support.
- **Comprehensive Dashboard:** Analytics and insights at a glance.

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 19 (Vite)
- **Styling:** Tailwind CSS (Modern Glassmorphism Design)
- **Icons:** Lucide React & React Icons
- **State Management:** React Hooks & Local Storage

### Backend
- **Framework:** Python Flask
- **Database:** MongoDB (using Pymongo)
- **Email Service:** Flask-Mail (for OTPs and Notifications)
- **Environment Management:** Python-Dotenv

---

## 🚀 Getting Started

Follow these steps to get the project up and running locally.

### Prerequisites
- Python 3.8+
- Node.js (LTS)
- MongoDB Account (or local instance)

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables in `.env`:
   ```env
   MONGO_URI=your_mongodb_uri
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email
   MAIL_PASSWORD=your_app_password
   ```
5. Start the server:
   ```bash
   python3 app.py
   ```

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## 📁 Project Structure

```text
ParkMate/
├── backend/            # Flask API & MongoDB Models
│   ├── routes/         # API Endpoints
│   ├── models/         # Database Schemas
│   └── app.py          # Entry Point
├── frontend/           # React Application
│   ├── src/
│   │   ├── Components/ # Reusable UI Components
│   │   ├── pages/      # Application Pages
│   │   └── services/   # API Integration
│   └── public/         # Static Assets
└── docs/               # Project Documentation & Images
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ by the ParkMate Team</p>
