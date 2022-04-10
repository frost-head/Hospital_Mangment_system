import re
from flask import Flask, redirect, render_template, request, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os
from database import *


app = Flask(__name__)
mysql = MySQL(app)
bcrypt = Bcrypt(app)

app.config['SERVER_NAME'] = 'localhost:5000'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ.get("Mysql_user")
app.config['MYSQL_PASSWORD'] = os.environ.get("Mysql_pass")
app.config['MYSQL_DB'] = 'hospital_managment'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/patientLogin', methods=['GET', 'POST'])
def patientlogin():
    if 'user' in session:
        flash('Already loged in', 'danger')
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        passcode = request.form['password']
        data = fetchone(
            mysql, "select pid, password from patient where email = '{}'".format(email))

        if data:
            password = data['password']
            uid = data['pid']

            if bcrypt.check_password_hash(password, passcode):
                password = data['password']
                uid = data['pid']

                session['user'] = uid
                flash('Successfully logged in', 'success')
                return redirect('/')
            else:
                flash('Invalid Password', 'danger')
        else:
            flash('User not Found', 'danger')

    return render_template('Login.html')


@app.route('/patientRegister', methods=['GET', 'POST'])
def patientRegister():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        mailtest = fetchone(
            mysql, "select pid from patient where email = '{}'".format(email))
        if mailtest:
            return "Email already registrer"
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        if request.form['bloodG']:
            bloodG = request.form['bloodG']
        else:
            bloodG = 'N/A'
        if request.form['fatherN']:
            fatherN = request.form['fatherN']
        else:
            fatherN = 'N/A'
        if request.form['address']:
            address = request.form['address']
        else:
            address = 'N/A'

        insert(mysql, "insert into patient(name, email, password, blood_group, father_name,address, age) values('{}', '{}','{}','{}','{}','{}',{})".format(
            name, email, pw_hash, bloodG, fatherN, address, age))

        uid = fetchone(
            mysql, "select pid from patient where email = '{}'".format(email))
        if uid:
            session['user'] = uid['pid']
            print(uid)
        return redirect('/')

    return render_template('Register.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect('/')
    return redirect('/patientLogin')


@app.route('/staffRegister', subdomain='staff', methods=['GET','POST'])
def staffRegister():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        desg = request.form['desg']
        mailtest = fetchone(
            mysql, "select sid from staff where email = '{}'".format(email))
        if mailtest:
            return "Email already registrer"
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        number = request.form['number']
        if request.form['address']:
            address = request.form['address']
        else:
            address = 'N/A'

        insert(mysql, "insert into staff(name, email, password, number, address, desg) values('{}', '{}','{}','{}','{}','{}')".format(
            name, email, pw_hash,number, address, desg))

        uid = fetchone(
            mysql, "select sid from staff where email = '{}'".format(email))
        if uid:
            session['user'] = uid['sid']
            print(uid)
        return redirect('/')

    return render_template('StaffRegister.html')

@app.route('/staffLogin', subdomain='staff' ,methods=['GET', 'POST'])
def stafflogin():
    if 'user' in session:
        flash('Already loged in', 'danger')
        return redirect('/staffDashboard')

    if request.method == 'POST':
        email = request.form['email']
        passcode = request.form['password']
        data = fetchone(
            mysql, "select sid, password from staff where email = '{}'".format(email))

        if data:
            password = data['password']
            uid = data['sid']
            session['user'] = uid
            flash('Successfully logged in', 'success')
            return redirect('/staffDashboard')
        else:
            flash('Invalid Password', 'danger')
    else:
        flash('User not Found', 'danger')

    return render_template('staffLogin.html')

@app.route('/logout', subdomain='staff')
def stafflogout():
    if 'user' in session:
        session.pop('user')
        return redirect('/')
    if 'user' not in session:
        return redirect('/staffLogin')

@app.route('/staffDashboard', subdomain="staff")
def staffDashboard():
    if 'user' not in session:
        return redirect("/staffLogin")
    data = fetchone(mysql, "select * from staff where sid = {}".format(session['user']))
    return render_template('staffDashboard.html', data=data)

@app.route('/patientDashboard')
def patientDashboard():
    if 'user' not in session:
        return redirect("/patientLogin")
    patientData = fetchone(mysql, "select * from patient where pid = {}".format(session['user']))
    vitalsData = fetchall(mysql, "select * from vitals where pid = {}".format(session['user']))
    print(vitalsData)
    return render_template('patientDashboard.html',patientData=patientData, vitalsData=vitalsData)

@app.route('/staffAddVitals', subdomain='staff', methods=['GET', 'POST'])
def staffAddVitals():
    if 'user' not in session:
        return redirect('/staffLogin')
    if request.method == 'POST':
        pid = request.form['pid']
        temp = request.form['temp']
        pulse = request.form['pulse']
        bp = request.form['bp']
        rr = request.form['rr']
        spo2 = request.form['spo2']
        weight = request.form['weight']
        sid = session['user']
        insert(mysql,"insert into vitals(pid, temp, pulse, blood_pressure, resp_rate, spo2, sid, weight) values({},{},{},{},{},{},{},{})".format(pid, temp, pulse, bp, rr, spo2, sid, weight))
        return redirect('/staffDashboard')
    return render_template('staffAddVitals.html')

app.run(debug=True, host='0.0.0.0')
