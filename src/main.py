import json
from datetime import datetime
from flask import Flask, redirect, render_template, request, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os
from database import *
from dotenv import load_dotenv
import requests
from markdown import markdown

load_dotenv()

app = Flask(__name__)
mysql = MySQL(app )
bcrypt = Bcrypt(app)

print("User:", os.environ.get("Mysql_user"))
print("Pass:", os.environ.get("Mysql_pass"))


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ.get("Mysql_user")
app.config['MYSQL_PASSWORD'] = os.environ.get("Mysql_pass")
app.config['MYSQL_DB'] = 'hospital_management'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    return render_template('Home.html', navless=True)


@app.route('/patientRegister', methods=['GET', 'POST'])
def patientRegister():

    if 'user' in session:
        flash('Already loged in', 'bad')
        return redirect('/patientDashboard')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        age = request.form['age']
        mailtest = fetchone(
            mysql, "select pid from patient where email = '{}'".format(email))
        if mailtest:
            flash("Email already registered", 'bad')

        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        

        insert(mysql, "insert into patient(email, password, name, number, age) values('{}', '{}','{}','{}','{}')".format(
            email, pw_hash, name, number, age))

        uid = fetchone(
            mysql, "select pid from patient where email = '{}'".format(email))
        if uid:
            session['user'] = uid['pid']
            flash("Successfully created an account", 'good')
        return redirect('/patientDashboard')

    return render_template('patientRegister.html', navless=True)


@app.route('/patientLogin', methods=['GET', 'POST'])
def patientlogin():
    if 'user' in session:
        flash('Already loged in', 'bad')
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
                flash('Successfully logged in', 'good')
                return redirect('/patientDashboard')
            else:
                flash('Invalid Password', 'bad')
        else:
            flash('User not Found', 'bad')

    return render_template('patientLogin.html', navless=True)


@app.route('/staffRegister', methods=['GET', 'POST'])
def staffRegister():

    if 'staff' in session:
        flash('Already loged in', 'good')
        return redirect('/staffDashboard')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        desg = request.form['desg']
        mailtest = fetchone(
            mysql, "select sid from staff where email = '{}'".format(email))
        if mailtest:
            flash("Email already registered", 'bad')
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
            session['staff'] = uid['sid']
            flash("successfully Registered", 'good')
        return redirect('/staffDashboard')

    return render_template('StaffRegister.html', navless=True)


@app.route('/staffLogin', methods=['GET', 'POST'])
def stafflogin():
    if 'user' in session:
        flash('Already loged in', 'bad')
        return redirect('/staffDashboard')

    if request.method == 'POST':
        email = request.form['email']
        passcode = request.form['password']
        data = fetchone(
            mysql, "select sid, password from staff where email = '{}'".format(email))

        if data:
            password = data['password']
            if bcrypt.check_password_hash(password, passcode):
                password = data['password']
                uid = data['sid']

                session['staff'] = uid
                flash('Successfully logged in', 'good')
                return redirect('/staffDashboard')
        else:
            flash('Invalid Password', 'bad')
    else:
        flash('User not Found', 'bad')

    return render_template('staffLogin.html', navless=True)


@app.route('/logout')
def logout():

    if('user' in session.keys()):
        if 'user' in session:
            session.pop('user')
            flash("Successfully logged out", 'good')
            return redirect('/')
        if 'user' not in session:
            flash("Not logged in", 'bad')
            return redirect('/')

    if('staff' in session.keys()):
        if 'staff' in session:
            session.pop('staff')
            flash("Successfully logged out", 'good')
            return redirect('/')
        if 'staff' not in session:
            flash("Not logged in", 'bad')
            return redirect('/')
    

@app.route('/staffDashboard')
def staffDashboard():
    if 'staff' not in session:
        flash('Not Logged in', 'bad')
        return redirect("/staffLogin")
    # session['staff'] = 1
    # appointments = fetchall(
        # mysql, """select staff.sid, staff.name, desg, app_id, patient.pid, date_time, patient.name from staff inner join appointments, patient where staff.sid = appointments.sid = {} and patient.pid = appointments.pid and date_time >= '{}' order by date_time asc""".format(session['staff'],datetime.now()))
    appointments = fetchall(mysql, """
    SELECT s.sid, s.name, s.desg, a.app_id, p.pid, a.date_time, p.name AS patient_name
    FROM staff s
    JOIN appointments a ON s.sid = a.sid
    JOIN patient p ON p.pid = a.pid
    WHERE s.sid = %s AND a.date_time >= %s
    ORDER BY a.date_time ASC
""", (session['staff'], datetime.now()))

    print(appointments)

    personal = fetchone(mysql, "select * from staff where sid = {}".format(session['staff']))

    # pateint = fetchall(mysql,"select * from patient where sid = 1;")
    pateint = fetchall(mysql, """
    SELECT p.*
    FROM patient AS p
    JOIN appointments AS a ON p.pid = a.pid
    WHERE a.sid = %s
""", (session['staff'],))

    print(personal)
    print(pateint)
    print(appointments)

    print(session['staff'])

    data = [appointments, personal, pateint]

    return render_template('staffDashboard.html', data=data)


@app.route('/patientDashboard')
def patientDashboard():
    if 'user'  not in session:
        flash('Not Logged in', 'bad')
        return redirect("/patientLogin")
    patientData = fetchone(
        mysql, "select * from patient where pid = {}".format(session['user']))
    vitalsData = fetchall(
        mysql, "select * from vitals where pid = {}".format(session['user']))
    appointments = fetchall(mysql, """select patient.pid, patient.email, patient.name, patient.number, patient.age, app_id, staff.sid , date_time, staff.name  from patient inner join appointments, staff where patient.pid = appointments.pid = {} and appointments.sid = staff.sid order by date_time asc""".format(session['user']))
    summary_row = fetchone(mysql,
        "SELECT summary, updated_at FROM patient_summary WHERE pid = %s",
        (session['user'],)
    )
    summary = summary_row['summary'] if summary_row else "No summary yet."
    last_updated = summary_row['updated_at'] if summary_row else None

    return render_template(
        'patientDashboard.html',
        patientData=patientData,
        vitalsData=vitalsData,
        appointments=appointments,
        summary=summary,
        last_updated=last_updated
    )

@app.route('/staffAddVitals', methods=['GET', 'POST'])
def staffAddVitals():
    if 'staff' not in session:
        flash('Not Logged in', 'bad')
        return redirect('/staffLogin')
    if request.method == 'POST':
        # 1) insert the new vital record
        pid     = request.form['pid']
        temp    = request.form['temp']
        pulse   = request.form['pulse']
        bp      = request.form['bp']
        rr      = request.form['rr']
        spo2    = request.form['spo2']
        weight  = request.form['weight']
        sid     = session['staff']

        insert(mysql,
            "INSERT INTO vitals "
            "(pid, temp, pulse, blood_pressure, resp_rate, spo2, weight, sid) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (pid, temp, pulse, bp, rr, spo2, weight, sid)
        )

        # 2) fetch the newly inserted vitals (you could also build your own string)
        new_vitals = fetchone(mysql,
            "SELECT temp,pulse,blood_pressure,resp_rate,spo2,weight,datetime "
            "FROM vitals WHERE vid = LAST_INSERT_ID()"
        )

        # 3) assemble prompt: include prior summary
        existing = fetchone(mysql,
            "SELECT summary FROM patient_summary WHERE pid = %s", (pid,)
        )
        if existing:
            prompt = (
                f"Previous summary: {existing['summary']}\n"
                f"New vitals: {new_vitals}\n"
                "Update the summary noting improvements or concerns."
            )
            updated = call_gemini(prompt)
            # update row
            update(mysql,
                "UPDATE patient_summary SET summary=%s, updated_at=NOW() WHERE pid=%s",
                (updated, pid)
            )
        else:
            prompt = f"New vitals for patient {pid}: {new_vitals}\nProvide a concise summary."
            initial = call_gemini(prompt)
            insert(mysql,
                "INSERT INTO patient_summary(pid, summary) VALUES (%s,%s)",
                (pid, initial)
            )

        return redirect('/staffDashboard')
    return render_template('staffAddVitals.html')

@app.template_filter('md2html')
def md2html(text):
    return markdown(text)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

def call_gemini(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_KEY
    }
    body = {"contents":[{"parts":[{"text":prompt}]}]}
    resp = requests.post(GEMINI_URL, headers=headers, json=body)
    resp.raise_for_status()
    data = resp.json()

    # (Optional) inspect it once
    print("=== GEMINI RESPONSE ===")
    print(json.dumps(data, indent=2))

    candidates = data.get("candidates", [])
    if not candidates:
        raise ValueError("No candidates in Gemini response")

    first = candidates[0]

    # 1) Top‑level flat content/output
    for key in ("output", "content"):
        if key in first and isinstance(first[key], str):
            return first[key]

    # 2) If 'content' is a dict (as in your latest test)
    if "content" in first and isinstance(first["content"], dict):
        content = first["content"]

        # a) maybe there's a 'text' field
        if "text" in content and isinstance(content["text"], str):
            return content["text"]

        # b) or a 'parts' list
        parts = content.get("parts")
        if isinstance(parts, list) and parts:
            text = parts[0].get("text")
            if isinstance(text, str):
                return text

    # 3) Finally, check if first itself has a 'parts' list
    parts = first.get("parts")
    if isinstance(parts, list) and parts:
        text = parts[0].get("text")
        if isinstance(text, str):
            return text

    # nothing matched
    raise ValueError(f"Couldn't extract text from Gemini response; candidate keys were {list(first.keys())}")


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if "user" not in session:
        flash('Not Logged in', 'bad')

        return redirect("/patientLogin")

    if request.method == 'POST':

        return redirect('/appointment/{}/{}/{}'.format(request.form['sid'], request.form['date'], request.form['time']))
    staffData = fetchall(mysql, "select sid, name from staff where desg = 0")
    print(staffData)

    return render_template("appointments.html", staffData=staffData)


@app.route('/appointment/<sid>/<date>/<time>', methods=['GET', 'POST'])
def appointment(sid, date, time):
    if "user" not in session:
        flash('Not Logged in', 'bad')

        return redirect("/patientLogin")
    appointmentData = fetchone(
        mysql, "select * from appointments where sid = {} and date_time = '{} {}'".format(sid, date, time))
    bookData = [sid, date, time]
    return render_template('appoinment.html', appointmentData=appointmentData, bookData=bookData)


@app.route('/bookAppointment/<sid>/<date>/<time>')
def bookAppointment(sid, date, time):
    if "user" not in session:
        flash('Not Logged in', 'bad')

        return redirect("/patientLogin")
    insert(mysql, "insert into appointments(sid, pid, date_time) values({},{},'{} {}');".format(
        sid, session['user'], date, time))
    return redirect("/patientDashboard")


@app.route('/store', methods=['GET', 'POST'])
def store():
    if "user" not in session:
        flash('Not Logged in', 'bad')


        return redirect("/patientLogin")

    items = fetchall(mysql, "select * from store")
    if request.method == 'POST' and 'qty' in request.form:
        qty = request.form['qty']
        item_id = request.form['item_id']
        old_qty = fetchone(
            mysql, "select * from cart where item_id = {} and pid = {}".format(item_id, session['user']))
        if old_qty is None:
            return storeRedirect(item_id, qty)
        else:
            qty = int(qty) + old_qty['pqty']
            update(mysql, 'update cart set pqty = {} where item_id = {} and pid = {}'.format(
                qty, item_id, session['user']))

    if request.method == 'POST' and 'search' in request.form:
        search_name = request.form['search']
        sql   = "SELECT * FROM store WHERE name LIKE %s"
        param = f"%{search_name}%"
        items = fetchall(mysql, sql, (param,))


    return render_template('store.html', items=items)


@app.route("/storeRedirect/<itemid>/qty")
def storeRedirect(itemid, qty):
    insert(mysql, "insert into cart(item_id, pid, pqty) values({},{},{})".format(
        itemid, session['user'], qty))
    flash('Added Successfully', 'good')
    
    return redirect('/store')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if "user" not in session:
        flash('Not Logged in', 'bad')

        return redirect("/patientLogin")

    items = fetchall(
        mysql, "select * from store inner join cart on store.item_id = cart.item_id where pid = {}".format(session['user']))

    amount = 0
    count = 0
    for item in items:
        amount += (item['price'] * item['pqty'])
        count += 1

    if request.method == 'POST':
        item_id = request.form['item_id']
        delete(mysql, 'delete from cart where item_id = {} and pid = {}'.format(
            item_id, session['user']))
        return redirect("/cart")

    return render_template('cart.html', items=items, amount=amount, count=count)


@app.route("/payment")
def payment():
    return render_template('payment.html')

@app.route("/patientStat/<pid>")
def patientStat(pid):
    data = fetchall(mysql,"select * from vitals where vitals.pid =  {}".format(pid))
    pdata = fetchone(mysql, "select * from patient where pid ={}".format(pid))
    temps = []
    bp = []
    resp = []
    spo2 = []
    weight = []
    label = []
    for vital in data:
        temps.append(int(vital['temp'])) 
        bp.append(vital['blood_pressure'])
        resp.append(vital['resp_rate'])
        spo2.append(vital['spo2']) 
        weight.append(vital['weight'])
        date = vital['datetime']
        
        label.append(date)

    # data = [bp, label]

    return render_template('Stats.html', data=data, pdata=pdata)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
