from flask import Flask, flash, redirect, render_template, request, session, url_for, json
import mysql.connector
import os
import json
import random
import datetime
from datetime import timedelta
from send_notification import send_notification
from glucose_insulin_trends import calculateTrend


app = Flask(__name__)

mydb = mysql.connector.connect(
  host="mydbinstance.clv2txpsdfyb.us-east-1.rds.amazonaws.com",
  user="admin",
  passwd="Mani1232",
  database="adms_aws"
)
mycursor = mydb.cursor()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('adms-2.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    sql = "SELECT * FROM adms_aws.patient_details where p_email=\'%s\';" % (str(request.form['username']))
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if not result:
        # flash('Invalid Username', 'warning')
        return render_template('login.html')
    else:
        result = list(result[0])
        if result[9] == request.form['username']:
            if result[10] == request.form['password']:
                session['logged_in'] = True
                # g_sql = "SELECT glucose_value from adms_aws.glucose_readings where patient_id=\'%s\';" % (result[0])
                # mycursor.execute(g_sql)
                # g_result = mycursor.fetchone()
                # if g_result:
                #     glocuse_reading = g_result[0]
                # else:
                #     glocuse_reading = 0
                latest_g_value = random.randrange(50, 90, 5)
                trend = update_trend(result[0], latest_g_value)
                latest_g_value = str(latest_g_value)
                g_update_sql = "UPDATE adms_aws.glucose_readings SET glucose_value= \'%s\', updated_time=\'%s\' " \
                               "WHERE patient_id= \'%s\';" % (latest_g_value, datetime.datetime.now(), result[0])
                mycursor.execute(g_update_sql)
                mydb.commit()
                i_sql = "SELECT * FROM glucose_readings WHERE patient_id=\'%s\'" % (result[0])
                mycursor.execute(i_sql)
                i_result = mycursor.fetchone()
                # updated_time = datetime.datetime.strptime(i_result[2], '%Y-%m-%d %H:%M:%S')
                print(calculateTrend(int(i_result[0]), datetime.datetime.now() + datetime.timedelta(hours=12), int(latest_g_value), i_result[2]))
                return render_template('adms-2.html', user=result[1], glocuse_reading=latest_g_value, trend_0=trend[0]
                                       , trend_1=trend[1], trend_2=trend[2], trend_3=trend[3], trend_4=trend[4])
            else:
                flash('Wrong password!', 'warning')
                return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if request.form['password'] == 'password' and request.form['username'] == 'admin':
    #     session['logged_in'] = True
    # else:
    #     flash('wrong password!')
    if not session.get('logged_in'):
        return render_template('sign-up.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        _first_name = request.form['fname']
        _last_name = request.form['lname']
        _email = request.form['email']
        _password = request.form['psw']
        _password_repeat = request.form['psw-repeat']
        _gender = request.form['gender']
        _dob = request.form['dob']
        _address1 = request.form['address1']
        _address2 = request.form['address2']
        _city = request.form['city']
        _state = request.form['state']
        _zip = request.form['zipcode']
        if _password != _password_repeat:
            return json.dumps({'html': '<span>Passwords should match!!</span>'})
        else:
            sql = "INSERT INTO patient_details (patient_id, p_f_name, p_gender, p_l_name, p_dob, p_address, p_city," \
                  " p_state, p_zip, p_email, p_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            temp_dob = _dob.replace('-', '')
            patient_id = str(temp_dob)+str(_zip)
            address = _address1 + " " + _address2
            val = (patient_id, _first_name, _gender, _last_name, _dob, address, _city, _state, _zip, _email, _password)
            mycursor.execute(sql, val)
            mydb.commit()
            # inserting dummy glucose values in to glucose_readings tables once patient is registered
            g_sql = "INSERT INTO glucose_readings(glucose_value, patient_id, updated_time) VALUES(%s, %s, %s)"
            g_val = (0, patient_id, datetime.datetime.now())
            mycursor.execute(g_sql, g_val)
            mydb.commit()
            # inserting dummy glucose values in to glucose_readings tables once patient is registered
            send_notification(_first_name, _email)
        return render_template('login.html')
    else:
        flash('Registration Unsuccessful!')
        print('check you input data.')
        return render_template('sign-up.html')


@app.route('/sign_out')
def sign_out():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('home'))


def update_trend(patient_id, latest_reading):
    with open('glucose_trends.json', 'r') as f:
        glucose_readings = json.load(f)
        if patient_id in glucose_readings['trends'].keys():
            trend = glucose_readings['trends'][patient_id]
            trend.pop(0)
            trend.append(latest_reading)
            glucose_readings['trends'][patient_id] = trend
        else:
            glucose_readings['trends'][patient_id] = [0, 0, 0, 0, 0]
    with open('glucose_trends.json', 'w') as f:
        json.dump(glucose_readings, f, indent=4)
    with open('glucose_trends.json', 'r') as f:
        glucose_readings = json.load(f)
        trend = glucose_readings['trends'][patient_id]
    return trend


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
