# ✈️ ALX Travel App

The ALX Travel App is a Django-based booking platform that allows users to explore property listings, make bookings, and leave reviews. This project is designed to showcase practical backend skills including REST API design, model relationships, seeding, and containerization.

---

## 🚀 Features

* 🔍 View and manage **property listings**
* 🗕️ Create and track **bookings**
* ⭐ Leave and read **reviews** for listings
* 🔐 Integrated with Django’s built-in User model
* 🛠 Powered by Django REST Framework
* 🧪 Seeder to populate sample data
* 🐳 Dockerized for easy local development

---

## 🧱 Tech Stack

* Python 3.10+
* Django 4.x
* Django REST Framework
* PostgreSQL or SQLite (dev)
* Docker & Docker Compose
* Faker (for seeding)

---

## 🗂 Project Structure

```bash
alx-travel_app/
├── listings/                 # App for listings, bookings, reviews
│   ├── models.py             # Listing, Booking, Review models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # DRF views (optional)
│   ├── urls.py               # App-specific URLs
│   └── management/
│       └── commands/
│           └── seed.py       # Seeder script using Faker
├── alx_travel_app/               # Main Django project settings
│   ├── settings.py
│   └── urls.py
├── db.sqlite3                # Default dev database
├── manage.py
├── Dockerfile                # (Optional) Docker image config
├── docker-compose.yml        # (Optional) Multi-service config
└── README.md                 # You're here!
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/alx-travel.git
cd alx-travel
```

### 2. Set up virtual environment

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed sample data

```bash
python manage.py seed
```

### 5. Run development server

```bash
python manage.py runserver
```

---

## 🐳 Docker Setup (Optional)

```bash
docker-compose up --build
```

---

## 👨‍💼 Author

Built with ❤️ by ALX student for backend training.

---

## 📄 License

This project is for educational use under the ALX Software Engineering Program.
