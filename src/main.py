from crypt import methods
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_bcrypt import bcrypt
import os
from database import *


app = Flask(__name__)
mysql = MySQL(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ.get("Mysql_user")
app.config['MYSQL_PASSWORD'] = os.environ.get("Mysql_pass")
app.config['MYSQL_DB'] = 'hospital_managment'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(24)


@app.route('/')
def home():
    return "<h1>Project Setup</h1>"


@app.route('/patientRegister', methods=['GET','POST'])
def patientRegister():

        
    return render_template('Register.html')

app.run(debug=True, host='0.0.0.0')
