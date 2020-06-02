from flask import Flask, render_template, request
from com.nico.webapp.data.postgresdb import save, return_data, initdb

app = Flask(__name__)
initdb()


@app.route('/')
def index():
    return render_template('home_page.html')

@app.route('/about')
def home():
    return render_template("about_page.html")

@app.route('/contact')
def contact():
    return render_template("contact_page.html")


@app.route('/register_post', methods = ['POST'])
def register_post_data():
    if request.method == 'POST':
        person_name = request.form['username']
        person_familly_name = request.form['familyname']
        person_age = request.form['age']
        person_birthday = request.form['birthday']
        person_hobby = request.form['hobbies_person_register']
        person_email = request.form['email']
        person_password = request.form['password']
        person_adding_new_hobby = request.form['new_hobby_person_register']
        print(person_name,
              person_familly_name,
              person_age, person_birthday,
              person_hobby,
              person_adding_new_hobby,
              person_email,
              person_password)
        save(person_name,
             person_familly_name,
             person_age, person_birthday,
             person_hobby,
             person_adding_new_hobby,
             person_email,
             person_password)
    return render_template("register.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/registered')
def vieuw_registered():
    return render_template("registered.html", nameee = return_data())
 #                                             '''
#                                             ["name"],
 #                                             familly = return_data['familly'],
  #                                            age = return_data['age'],
   #                                           birthday = return_data('birthday'),
    #                                          hobbies = return_data('hobby'),
     #                                         email = return_data('email'))
      #                                        '''


if __name__ == '__main__':
     app.run(debug=True)