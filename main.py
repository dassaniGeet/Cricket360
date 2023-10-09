from flask import Flask, request, render_template, redirect, url_for
from database import Database
import threading
from API import send_sms, check_phoneno
from time import sleep
 
app = Flask(__name__, template_folder='templates')

db = Database()
data_users = []

@app.route('/', methods=['GET']) 
def index(): 
    return render_template('index.html')

@app.route('/action', methods=['POST'])
def action():
    name = request.form['userName']
    phoneno = request.form['userContact']
    action = request.form['action']

    if action == 'register':
        # Redirect to endpoint 1
        return redirect(url_for('register', name=name, phoneno=phoneno))
    elif action == 'unregister':
        # Redirect to endpoint 2
        return redirect(url_for('unregister', phoneno=phoneno))
    else:
        # Handle other actions if necessary
        pass

@app.route('/register')
def register():
    name = request.args.get('name')
    phoneno = request.args.get('phoneno')
    global data_users
    for data in data_users:
        if phoneno == data[2]:
            msg = "Already a registered user."
            return render_template('page.html', params = msg)

    valid_phoneno = check_phoneno(phoneno)
    if valid_phoneno == 0:
        msg = "Invalid Phone Number or Verification Call not answered.\nTry Again!"
        return render_template('page.html', params = msg)
    
    # Todo: UI

    db.insert_value(name, phoneno)

    data_users = db.fetch_data()
    msg = "Registration Sucessfull! You will be notified regularly."
    return render_template('page.html', params = msg)
    
@app.route('/unregister')
def unregister():
    phoneno = request.args.get('phoneno')
    flag=0
    global data_users
    for data in data_users:
        if phoneno == data[2]:
            db.delete_data(data[0])
            flag=1
            break
    if flag==0:
        msg = "Phone No. Not Registered."
        return render_template('page.html', params = msg)
    else:
        data_users = db.fetch_data()
        msg = "UnRegistered Sucessfully! Hope You Enjoyed:)"
        return render_template('page.html', params = msg)
       
def send_updates():
    while(True):
        numbers = []
        for data in data_users:
            numbers.append(data[2])
        send_sms(numbers)
        sleep(900)

 
if __name__ == '__main__':
    network_thread = threading.Thread(target=send_updates)
    network_thread.daemon = True 
    network_thread.start()
    app.run(debug=True)
