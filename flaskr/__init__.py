from flask import Flask, render_template, redirect, url_for, session, request, make_response, Blueprint
from datetime import timedelta
import mysql.connector



app = Flask(__name__, template_folder='template')
app.secret_key = "dev"
app.permanent_session_lifetime = timedelta(minutes=1)

# app.register_blueprint(auth.bq)

@app.route('/')
def login():
    return render_template('/login.html')


@app.route('/home')
def home():
    return render_template('/home.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/info',  methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        name = request.form['name']
        ticket_no = request.form['ticket_no']

        connectie = mysql.connector.connect(
            user='admin',
            password='odroid',
            host='192.168.3.2',
            database='mydb'
        )
        cursor = connectie.cursor()
        query = "SELECT name, ticket_no FROM login_informations WHERE name = %s and ticket_no = %s"
        param = (name, ticket_no)
        cursor.execute(query, param)
        entry = cursor.fetchone()
        connectie.close()

        # check if something returned
        if entry:
            ip_addr = request.remote_addr

            session['name'] = name
            session['ticket_no'] = ticket_no
            return redirect(url_for('home'))
        else:
            session.clear()
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)