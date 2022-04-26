# from crypt import methods
from re import template
from flask import Flask, redirect, render_template, request, flash, session, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os
from database import *


app = Flask(__name__)
mysql = MySQL(app)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ.get("Mysql_user")
app.config['MYSQL_PASSWORD'] = os.environ.get("Mysql_pass")
app.config['MYSQL_DB'] = 'hospital_managment'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    return render_template('Home.html', navless=True)


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
        number = 0

        insert(mysql, "insert into patient(email, password, name, number, address, blood_group, father_name, age) values('{}', '{}','{}','{}','{}','{}','{}','{}')".format(
            email, pw_hash, name, number,  address, bloodG, fatherN, age))

        uid = fetchone(
            mysql, "select pid from patient where email = '{}'".format(email))
        if uid:
            session['user'] = uid['pid']
            print(uid)
        return redirect('/')

    return render_template('patientRegister.html', navless=True)


@app.route('/patientLogin', methods=['GET', 'POST'])
def patientlogin():
    if 'user' in session:
        flash('Already loged in', 'danger')
        return redirect('/patientDashboard')

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
                return redirect('/patientDashboard')
            else:
                flash('Invalid Password', 'danger')
        else:
            flash('User not Found', 'danger')

    return render_template('patientLogin.html', navless=True)


@app.route('/staffRegister', methods=['GET', 'POST'])
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
            name, email, pw_hash, number, address, desg))

        uid = fetchone(
            mysql, "select sid from staff where email = '{}'".format(email))
        if uid:
            session['user'] = uid['sid']
            print(uid)
        return redirect('/')

    return render_template('StaffRegister.html', navless=True)


@app.route('/staffLogin', methods=['GET', 'POST'])
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

    return render_template('staffLogin.html', navless=True)


@app.route('/logout')
def stafflogout():
    if 'user' in session:
        session.pop('user')
        return redirect('/')
    if 'user' not in session:
        return redirect('/')


@app.route('/staffDashboard')
def staffDashboard():
    if 'user' not in session:
        return redirect("/staffLogin")
    data = fetchone(
        mysql, "select * from staff where sid = {}".format(session['user']))
    return render_template('staffDashboard.html', data=data)


@app.route('/patientDashboard')
def patientDashboard():
    if 'user' not in session:
        return redirect("/patientLogin")
    patientData = fetchone(
        mysql, "select * from patient where pid = {}".format(session['user']))
    vitalsData = fetchall(
        mysql, "select * from vitals where pid = {}".format(session['user']))
    print(vitalsData)
    return render_template('patientDashboard.html', patientData=patientData, vitalsData=vitalsData)


@app.route('/staffAddVitals', methods=['GET', 'POST'])
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
        insert(mysql, "insert into vitals(pid, temp, pulse,  blood_pressure, resp_rate, spo2, sid, weight) values({},{},{},{},{},{},{},{})".format(
            pid, temp, pulse, bp, rr, spo2, sid, weight))
        return redirect('/staffDashboard')
    return render_template('staffAddVitals.html')


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if "user" not in session:
        return redirect("/patientLogin")

    if request.method == 'POST':

        return redirect('/appointment/{}/{}/{}'.format(request.form['sid'], request.form['date'], request.form['time']))
    staffData = fetchall(mysql, "select sid, name from staff where desg = 0")
    print(staffData)

    return render_template("appointments.html", staffData=staffData)


@app.route('/appointment/<sid>/<date>/<time>', methods=['GET', 'POST'])
def appointment(sid, date, time):
    if "user" not in session:
        return redirect("/patientLogin")
    appointmentData = fetchone(
        mysql, "select * from appointments where sid = {} and date_time = '{} {}'".format(sid, date, time))
    bookData = [sid, date, time]
    return render_template('appoinment.html', appointmentData=appointmentData, bookData=bookData)


@app.route('/bookAppointment/<sid>/<date>/<time>')
def bookAppointment(sid, date, time):
    if "user" not in session:
        return redirect("/patientLogin")
    insert(mysql, "insert into appointments(sid, pid, date_time) values({},{},'{} {}');".format(
        sid, session['user'], date, time))
    return redirect("/patientDashboard")


@app.route('/store', methods=['GET', 'POST'])
def store():
    # if "user" not in session:
    #     return redirect("/patientLogin")

    # for development purpose
    session['user'] = 1

    items = fetchall(mysql, "select * from store")
    print(items)
    cart = fetchall(
        mysql, "select * from cart where pid = {}".format(session['user']))
    print(cart)
    # item = request.form['item']
    # qty = request.form['qty']
    # if request.method == 'POST':
    #     insert(mysql, "insert into patient(item_id, pid, qty) values('{}', '{}', '{}')".format(
    #         item, session['user'], qty))
    return render_template('store.html', items=items)


app.run(debug=True, host='0.0.0.0')
