# 🐍 Student Grades Scraper

## Overview

This is a Python script that automates the extraction of student grades from the university website.
It logs in using a list of student usernames and passwords, collects their grades, and exports the results into a structured CSV file.

---

## Features

- 🔑 Automated login using student credentials.
- 📂 Retrieval of each student’s grades from the university portal.
- 📝 Export of results into a CSV file containing:

  - Student username
  - Extracted grades (ordered)

---

## Project Structure

```
├── app.py             # Main scraping script
├── requirements.txt   # Dependencies
├── README.md          # Documentation
└── .gitignore         # Ignore sensitive and unnecessary files
```

---

## Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yosefbeder/student-grades-scraper.git
cd student-grades-scraper
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv env
source env/bin/activate   # On Windows use: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Script

Create an `input.csv` file containing the following columns: NAME,PASSWORD,USERNAME.

```bash
python app.py
```

> ⚠️ **Important:**
>
> - Do not upload real usernames/passwords to GitHub.
> - Use only anonymized or test accounts when sharing code.

---

## License

This project is for **educational purposes only**.
