# 📞 Spam Detection REST API

A **production-ready backend API** for identifying spam phone numbers and caller details, inspired by apps like Truecaller.  
Built as a **real-world portfolio project** using modern backend best practices.

---

## 🚀 Live Demo
**Base URL**  
```
https://spam-detection-api-tk0g.onrender.com/api/
```

> ⚠️ Free Render instances may sleep after inactivity. First request can take ~30 seconds.

---

## 🧠 What This Project Does

This API allows users to:
- Register and log in securely using JWT authentication
- Mark phone numbers as spam
- Search phone numbers or names globally
- View spam likelihood for phone numbers
- Protect user privacy by limiting email visibility

Spam likelihood increases as more users report the same number.

---

## 🛠 Tech Stack

- **Backend**: Django 5, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: PostgreSQL (Render)
- **Hosting**: Render Cloud
- **ORM**: Django ORM (no raw SQL)

---

## 🔐 Authentication Flow

### Register
```
POST /register/
```
```json
{
  "username": "user0",
  "password": "password",
  "phone_number": "7788990044",
  "email": "user@gmail.com"
}
```

### Login
```
POST /login/
```
```json
{
  "username": "user0",
  "password": "password"
}
```

Response:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Authorization Header
All protected endpoints require:
```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 📌 API Endpoints

### Get Contacts (Protected)
```
GET /contacts/
```

Returns all contacts belonging to the authenticated user with spam likelihood.

---

### Mark a Number as Spam (Protected)
```
POST /mark-spam/
```
```json
{
  "phone_number": "9999999999"
}
```

Rules:
- A user can mark a number as spam only once
- Each spam report increases global spam likelihood by **0.1**

---

### Search by Name (Protected)
```
GET /search-by-name/?name=rahul
```

Behavior:
- Names starting with the query appear first
- Then partial matches

Email is returned **only if the searched contact exists in the user’s contact list**.

---

### Search by Phone Number (Protected)
```
GET /search-by-phone/?phone_number=9999999999
```

Behavior:
- Returns spam likelihood and basic info
- Email shown only for known contacts

---

## 📊 Spam Likelihood Logic

- Initial value: `0.0`
- Each spam report: `+0.1`
- Stored **globally per phone number**
- Aggregated from multiple users

---

## 🔒 Security & Best Practices

- Passwords hashed using Django’s `set_password()`
- JWT-based authentication
- Protected endpoints via `IsAuthenticated`
- Public endpoints explicitly allowed
- ORM-only database access
- Environment variables for secrets

---

## 🗄 Database Design

- Custom User model (phone-number centric)
- Separate tables for:
  - Users
  - Contacts
  - Global Contacts
  - Spam Marks
- Indexed phone number fields for fast lookup

---

## ⚙️ Running Locally

### Requirements
- Python 3.10+
- PostgreSQL

### Setup
```bash
git clone <repo-url>
cd spam-detection-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## ☁️ Deployment

- Deployed on **Render**
- Managed PostgreSQL instance
- Gunicorn as WSGI server
- Environment-based configuration

---

## 🎯 Why This Project Matters

This project demonstrates:
- Real-world authentication flows
- Scalable relational data modeling
- Secure API design
- Production deployment experience
- Debugging & problem-solving under real constraints

It is **not a tutorial project**, but a practical backend system built end-to-end.

---

## 👨‍💻 Author

**Akash Kumar**  
Backend Developer | Django | REST APIs

---

## 📌 Notes

- API-only project (no frontend)
- Suitable for mobile or web client integration
- Built for learning, portfolio, and real-world practice

---

⭐ If you like this project, feel free to star the repository!
