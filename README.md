# Hospital Management System

A web-based Hospital Management System built with Flask and MySQL, designed to streamline hospital operations for both patients and staff. The system supports appointment booking, patient and staff management, vitals tracking, an online pharmacy, and more.

## Features

### For Patients
- **Registration & Login:** Secure sign-up and login for patients.
- **Dashboard:** View personal details, medical vitals, and appointment history.
- **Book Appointments:** Schedule appointments with doctors online.
- **View Reports:** Access previous medical reports and vitals.
- **Online Pharmacy:** Browse and purchase medicines from the hospital store.
- **Cart & Payment:** Add medicines to cart and proceed to payment.

### For Staff
- **Registration & Login:** Secure sign-up and login for hospital staff.
- **Dashboard:** View upcoming appointments and assigned patients.
- **Add Patient Vitals:** Record and update patient vitals (temperature, pulse, blood pressure, etc.).
- **Patient Reports:** Access and visualize patient health statistics.

### General
- **Role-based Navigation:** Separate dashboards and navigation for patients and staff.
- **Responsive UI:** Modern, user-friendly interface.
- **Secure Passwords:** Passwords are hashed using bcrypt.
- **Session Management:** Secure session handling for users and staff.

## Tech Stack

- **Backend:** Python, Flask, Flask-MySQLdb, Flask-Bcrypt
- **Frontend:** HTML, CSS (custom, with responsive design), Jinja2 templates
- **Database:** MySQL
- **Other:** python-dotenv for environment variable management

## Project Structure

```
src/
  main.py           # Main Flask application
  database.py       # Database helper functions
  database.sql      # MySQL schema and sample data
  static/           # CSS, images, and other static assets
  templates/        # HTML templates (Jinja2)
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Hospital_Mangment_system
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Update your `requirements.txt` to include all dependencies:

```
Flask==2.0.2
Flask-MySQLdb
Flask-Bcrypt
python-dotenv
```

Then install:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `src/` directory with your MySQL credentials:

```
Mysql_user=your_mysql_username
Mysql_pass=your_mysql_password
```

### 5. Set Up the Database

- Ensure MySQL is running.
- Create a database named `hospital_management`.
- Import the schema and sample data:

```bash
mysql -u your_mysql_username -p hospital_management < src/database.sql
```

### 6. Run the Application

```bash
cd src
python main.py
```

The app will be available at `http://localhost:5000`.

## Usage

- Visit the home page to choose between patient and staff login.
- Patients can register, log in, book appointments, view reports, and shop for medicines.
- Staff can register, log in, view their dashboard, and add patient vitals.

## Screenshots

*(Add screenshots of the home page, dashboards, appointment booking, and store for better presentation.)*

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
