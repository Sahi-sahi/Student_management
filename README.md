# 🎓 Student Management System

A full-stack web application to manage student records with **Create, Read, Update, and Delete (CRUD)** operations — built with Flask, MySQL, and vanilla HTML/CSS/JS.

---

## 📁 Project Structure

```
student_management/
├── database/
│   └── schema.sql          ← Run once to create tables
├── backend/
│   ├── db_config.py        ← DB connection settings
│   ├── student_model.py    ← All DB operations (CRUD)
│   ├── app.py              ← Flask REST API server
│   └── requirements.txt    ← Python dependencies
└── frontend/
    └── index.html          ← Open in browser
```

---

## 🛠️ Tech Stack

| Layer     | Technology        |
|-----------|-------------------|
| Frontend  | HTML, CSS, JavaScript |
| Backend   | Python, Flask     |
| Database  | MySQL             |

---

## ⚙️ Prerequisites

Make sure the following are installed on your system:

- Python 3.8+
- MySQL Server
- pip (Python package manager)

---

## 🚀 Setup & Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/student_management.git
cd student_management
```

### Step 2 — Set Up the Database

1. Open your MySQL client (MySQL Workbench or terminal).
2. Create the database:

```sql
CREATE DATABASE myproject_db;
```

3. Run the schema file to create the tables:

```bash
mysql -u root -p myproject_db < database/schema.sql
```

---

### Step 3 — Configure Database Connection

Open `backend/db_config.py` and update your MySQL credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",              # your MySQL username
    "password": "yourpassword",  # your MySQL password
    "database": "myproject_db"
}
```

---

### Step 4 — Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### Step 5 — Start the Flask Server

```bash
python app.py
```

The API will be running at: **`http://127.0.0.1:5000`**

---

### Step 6 — Open the Frontend

Simply open the frontend file in your browser:

```
frontend/index.html
```

> Double-click the file **or** right-click → *Open with* → your browser.

---

## 🔌 API Endpoints

| Method | Endpoint             | Description            |
|--------|----------------------|------------------------|
| GET    | `/students`          | Get all students       |
| GET    | `/students/<id>`     | Get student by ID      |
| POST   | `/students`          | Add a new student      |
| PUT    | `/students/<id>`     | Update student details |
| DELETE | `/students/<id>`     | Delete a student       |

---

## 🗄️ Database

- **Database Name:** `myproject_db`
- **Schema File:** `database/schema.sql`

The schema file creates all required tables automatically. Run it **once** before starting the server.

---

## 📦 Python Dependencies (`requirements.txt`)

```
Flask
flask-cors
mysql-connector-python
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 🧪 Testing the API

You can test the API using tools like:

- [Postman](https://www.postman.com/)
- [Thunder Client](https://www.thunderclient.com/) (VS Code extension)
- `curl` in terminal:

```bash
# Get all students
curl http://127.0.0.1:5000/students
```

---

## 🐛 Common Issues

| Problem | Solution |
|---|---|
| `mysql.connector` error | Run `pip install mysql-connector-python` |
| `CORS` error in browser | Ensure `flask-cors` is installed and configured in `app.py` |
| Database connection failed | Check credentials in `db_config.py` |
| Port already in use | Change the port in `app.py`: `app.run(port=5001)` |

---

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)

---

## 📄 License

This project is open-source and free to use for educational purposes.
