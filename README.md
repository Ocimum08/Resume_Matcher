# 🧠 Resume Matcher - Flask Web App

Resume Matcher is a lightweight Flask-based web application that allows users to upload their resumes and compare them against job descriptions using keyword matching and similarity scoring. It's designed to help job seekers optimize their resumes for specific roles and increase their chances of selection.

## 🚀 Features

- 🔐 Login/Signup system (session-based)
- 🧾 Resume upload (PDF)
- 💼 Job description input field
- 🧠 Keyword and skill matching
- 📊 Match percentage calculation
- 📥 Downloadable result summary
- 🌙 Dark mode toggle with localStorage persistence
- 👤 User dashboard with session-based access
- ⚡ No database required
- 💻 Responsive UI with Tailwind CSS

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, Tailwind CSS
- **Resume Parsing:** `pdfminer` or similar libraries
- **Authentication:** Flask sessions (no DB)
- **Other:** File handling, string similarity logic, dark mode via `localStorage`

---

## 📁 Project Structure

RESUME_MATCHER/ ├── pycache/ # Python cache files ├── instance/ # Flask instance folder (config, if needed) ├── results/ # Folder to store match results ├── templates/ # HTML templates │ ├── base.html │ ├── dashboard.html │ ├── index.html │ ├── login.html │ ├── result.html │ └── signup.html ├── uploads/ # Uploaded resumes (PDF) │ └── UDIT_SHARMA.pdf # Example resume ├── venv/ # Python virtual environment ├── app.py # Main Flask application ├── models.py # Matching and processing logic ├── README.md # Project overview └── requirements.txt # Python dependencies


---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/resume-matcher.git
cd resume-matcher

## Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

## Run the Flask Server
python app.py

## Visit the app
http://127.0.0.1:5000