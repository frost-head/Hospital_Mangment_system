from hashlib import sha256, sha3_256
from flask import Flask, redirect, render_template, request, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os
from database import *


app = Flask(__name__)
mysql = MySQL(app)
bcrypt = Bcrypt(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'hospital'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    return "<h1>Project Setup</h1>"


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

        insert(mysql, "insert into patient(name, email, password, blood_group, father_name,address, age) values('{}', '{}','{}','{}','{}','{}','{}')".format(
            name, email, pw_hash, bloodG, fatherN, address, age))

        uid = fetchone(
            mysql, "select pid from patient where email = '{}'".format(email))
        if uid:
            session['user'] = uid['pid']
            print(uid)
        return redirect('/')

    return render_template('Register.html')


<< << << < HEAD
== == == =


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect('/')
    return redirect('/patientLogin')


>>>>>> > 49bc0f54ce9f260d6080c46ef6494a6fdcaad5f9

app.run(debug=True, host='0.0.0.0')
