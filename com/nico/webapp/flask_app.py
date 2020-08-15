import random

from flask import Flask, render_template, request, session, redirect, url_for

from com.nico.webapp.data.sqliteDB import save
from com.nico.webapp.data.sqliteDB import return_data
from com.nico.webapp.data.sqliteDB import initdb
from com.nico.webapp.data.sqliteDB import return_hobby
from com.nico.webapp.data.sqliteDB import return_name
from com.nico.webapp.data.sqliteDB import return_family
from com.nico.webapp.data.sqliteDB import return_age
from com.nico.webapp.data.sqliteDB import return_birthday
from com.nico.webapp.data.sqliteDB import return_email

from com.nico.webapp.emailBot import verification_email_sender


code = random.randint(1000, 9999)
files = []
app = Flask(__name__)
app.secret_key = '9\x8f\x8b\xeb\x85\xe3\xb3\xeaA\xae\x99=\xc8\x12\x8e[\x0f\x86\x94\xe0\xe8\x0e'
initdb()
i = 0
print(return_data())

@app.route('/')
def index():
    return render_template('home_page.html')


@app.route('/about')
def home():
    return render_template("about_page.html")


@app.route('/contact')
def contact():
    return render_template("contact_page.html", email = 'nicor1969.ryj@gmail.com')


@app.route('/register', methods=['POST'])
def register_post_data():
    if request.method == 'POST':
        print('====================================== REGISTRATION STARTED ======================================')
        person_name = request.form['username']
        person_familly_name = request.form['familyname']
        person_age = request.form['age']
        person_birthday = request.form['birthday']
        person_hobby = request.form['hobbies_person_register']
        global person_emailaddress
        person_emailaddress = request.form['email']
        session["user"] = person_emailaddress
        print(session['user'])
        person_password = request.form['password']
        person_adding_new_hobby = request.form['new_hobby_person_register']
        print(person_name,
              person_familly_name,
              person_age, person_birthday,
              person_hobby,
              person_adding_new_hobby,
              person_emailaddress,
              person_password)
        save(person_name,
             person_familly_name,
             person_age,
             person_birthday,
             person_hobby,
             person_adding_new_hobby,
             person_emailaddress,
             person_password)
    return render_template("register.html")


#emailaddress = person_emailaddress


@app.route('/confirm', methods=['GET', 'POST'])
def confirm_password():
    if request.method == 'POST':
        verification_email_sender('Verification code',
                                  'nicoryj.pythonbot@gmail.com',
                                  person_emailaddress,
                                  'Website made by flask with python',
                                  files,
                                  code,
                                  'Nicolas02_python')
        global i
        while i != 1:
            if code == request.form['password']:
                i = i + 1
                return redirect(url_for("vieuw_registered", name_data=return_data()))
            elif request.form['password'] != "" and code != request.form['password']:
                return render_template('wrong_pass.html')
            else:
                return render_template('confirm_pass.html')
    return render_template('confirm_pass.html', emailAddressUser = 'nicor1969.ryj@gmail.com')


@app.route('/register')
def register():
    return render_template("register.html", hobby_data = return_hobby())


@app.route('/wrong_pass')
def wrongPass():
    return render_template("wrong_pass.html")


@app.route('/registered')
def vieuw_registered():
    return render_template("registered.html",
                           name_data=return_name(),
                           name_family=return_family(),
                           name_age=return_age(),
                           name_birthday=return_birthday(),
                           name_email=return_email(),
                          )


@app.route('/logout')
def logout():
    global session
    session.pop("user", None)
    return render_template('logout.html')


if __name__ == '__main__':
     app.run(debug=True)
