from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, json, jsonify
import app
import mysql.connector
import os
import json
import pybase64

app = Flask(__name__)
mydb = mysql.connector.connect(
  host="mydbinstance.clv2txpsdfyb.us-east-1.rds.amazonaws.com",
  user="admin",
  passwd="Mani1232",
  database="adms"
)
mycursor = mydb.cursor()


@app.route('/register', methods=['POST'])
def register():
  if not session.get('logged_in'):
    return render_template('sign-up.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    try:
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
                resp = json.dumps('Passwords must match!')
            else:
                sql = "INSERT INTO patient_details (patient_id, p_f_name, p_gender, p_l_name, p_dob, p_address, p_city," \
                      " p_state, p_zip, p_email, p_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                temp_dob = _dob.replace('-', '')
                patient_id = str(temp_dob)+str(_zip)
                address = _address1 + _address2
                val = (patient_id, _first_name, _gender, _last_name, _dob, address, _city, _state, _zip, _email, _password)
                mycursor.execute(sql, val)
                mydb.commit()
                resp = json.dumps('User added successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)


@app.route('/patients')
def patients():
    try:
        response = dict()
        mycursor.execute("SELECT * FROM patient_details")
        result = mycursor.fetchall()
        resp = jsonify(result)
        resp.status_code = 200

        return resp
    except Exception as e:
        print(e)


@app.route('/patient/<int:patient_id>', methods=['GET'])
def patient(patient_id):
    try:
        response = {}
        mycursor.execute("SELECT * FROM patient_details WHERE patient_id=%s", (patient_id,))
        row = mycursor.fetchone()
        response = jsonify(row)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)


@app.route('/delete/<int:patient_id>', methods=['GET'])
def delete_patient(patient_id):
    try:
        response = {}
        mycursor.execute("DELETE FROM patient_details WHERE patient_id=%s", (patient_id,))
        mydb.commit()
        response = jsonify('Patient deleted successfully')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()
