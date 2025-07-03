# HomeGenie – Household Services Application

A modern, full-stack platform for booking and managing household services, built as part of the Modern Application Development - II (MAD-II) course.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Contributors](#contributors)
- [License](#license)

---

## Overview

**HomeGenie** is a web application for seamless household service management. The platform connects customers with verified service professionals and enables admins to oversee all activities. Built using Flask (backend) and Vue.js (frontend), HomeGenie ensures secure, efficient, and user-friendly service booking and management.

---

## Features

- **Secure Token-Based Authentication** for all users
- **Role-Based Dashboards** for Customers, Service Professionals, and Admins
- **Service Request System** with real-time status tracking
- **Admin Management:** Approve/reject professionals, manage users, create and update services
- **Search & Filter:** Find services by name, location, or pincode
- **Async CSV Export:** Export service request data efficiently
- **Automated Reminders & Reports:** Daily and monthly notifications using Celery and Redis
- **API Performance Optimization:** Redis caching and rate limiting
- **Responsive UI/UX:** Built with Vue.js and Bootstrap, including validation
- **Advanced Analytics:** Visualize service and user activity (recommended)
- **Payment Integration:** Dummy portal (optional)

---

## Tech Stack

- **Frontend:** Vue.js, Bootstrap
- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Background Tasks:** Celery, Redis
- **Authentication:** Token-based (JWT)
- **Other:** ChartJS (analytics), CSV export

---

## Setup Instructions

1. **Clone the repository:**
  ```
  git clone https://github.com/yourusername/HomeGenie.git
  cd HomeGenie
  ```

2. **Backend Setup:**
- Create a virtual environment and activate it.
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```

3. **Frontend Setup:**
- Navigate to the frontend directory:
  ```
  cd frontend
  npm install
  npm run serve
  ```

4. **Start Redis and Celery Workers:**
- Start Redis server.
- In a new terminal, start Celery worker:
  ```
  celery -A app.celery worker --loglevel=info
  ```

5. **Run Flask Backend:**
  ```
  python app.py
  ```

7. **Access the application:**  
- Visit `http://localhost:8080` for the frontend and `http://localhost:5000` for the backend API.

---

## Contributors

- **Deebhika Kumaran** – Backend, Frontend, System Integration

---

## License

This project is for educational purposes as part of the Modern Application Development - II course.

---
