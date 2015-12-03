from flask import Flask, request, url_for, redirect, session, flash, render_template
from functools import wraps
from flask import g
app = Flask(__name__)
app.secret_key = 'do you even lift'
from wtforms import Form, BooleanField, TextField, PasswordField, validators    
from passlib.hash import sha256_crypt


import data
data.init_db()


@app.route("/")
def homepage():
    return render_template ("home.html")

@app.route("/Workout")
def workout():
   return render_template("workouts.html")
@app.route("/Nutrition")
def nutrion():
   return render_template("nutrition.html")

@app.route("/Supplements")
def supplements():
    return render_template("supplements.html")
	
	
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
           flash("Sorry you need to log in first")
           return redirect(url_for('login'))
    return wrap
	
@app.route("/profile")
@login_required
def profile():
	return render_template("profile.html")
	
@app.route("/logout")
def out():
   session.pop('logged_out', None)
   if ("logout" != None):
       flash ("You are now logged out")
   return redirect (url_for('login')) 

@app.route("/Login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form ["username"] != "chris" or request.form ["password"] != "chris":
            error = "Wrong password or username. Please try again."
        else:
          session['logged_in']=True
          return redirect (url_for("cat"))
    return render_template("login.html", error=error)

#@app.route("/Login", methods=["GET", "POST"])
#def login():
   #error = None
   #conn = data.get_db()
   #if request.method == "POST":
     #username = request.form['username']
     #password = request.form['password']
    # sql = "SELECT username from users WHERE username= '"+username+"'"
    # if (len(conn.cursor().execute(sql).fetchall()) == 0):
     #error = "wrong username. please use another"

     #else:
       #session['logge_in']= True
       ##session['username']= username
       #return redirect(url_for('profile'))
	   #return render_template("login.html",form=form)
      


class RegistrationForm(Form):
	 username = TextField('Username', [validators.Length(min=4, max=20)])
	 
	 email = TextField('Email Address', [validators.Length(min=6, max=45)])
	 
	 password = PasswordField('password', [validators.Required(),])
                                  
	 confirm = PasswordField('Repeat Password', [validators.Required(), validators.EqualTo('password', message='Both password must match.')])
	 
	 accept_tos = BooleanField('I accept the Terms and Conditions', [validators.Required()])
	 
	 

	 

		

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(request.form)
  conn = data.get_db()

  if (request.method == 'POST'):
    username = form.username.data
    sql = "SELECT username from users WHERE username= '"+username+"'"
    if (len(conn.cursor().execute(sql).fetchall()) != 0):

      flash("user doesn't exist try again")
    else:
      email = form.email.data
      password = sha256_crypt.encrypt(str(form.password.data))
      sql = "INSERT INTO users (username, password, email) VALUES ('"+ username +"', '"+ password +"', '"+ email +"')"
      conn.cursor().execute(sql)
      conn.commit()
      flash("Thanks for joining")
      conn.cursor().close()
      conn.close()
    return redirect(url_for('profile'))
  else:
    return render_template('register.html', form = form)

@app.errorhandler(404)
def page_not_found(error):
   return "this page doen't exist" 
   
   

    
   

  
  
  
@app.errorhandler(405)
def methods_not_found(e): 
    return ("This method is not found!")
   
   
  
	
	
   
	
if __name__== "__main__":
    app.run(host='0.0.0.0', debug=True)
