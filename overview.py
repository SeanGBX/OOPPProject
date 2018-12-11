from flask import Flask, render_template, redirect, url_for, request, session, flash, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.secret_key = "keys"

#SQL Configs
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123admin123"
app.config["MYSQL_DB"] = "registerdb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# init MYSQL
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to be logged in first")
            return redirect(url_for("login"))
    return wrap

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/overview")
def overview():
    return render_template("overview.html")

class RegisterForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    username = StringField("Username", [validators.Length(min=3, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=50)])
    password = PasswordField("Password",[
        validators.DataRequired(),
        validators.EqualTo("confirm", message="Passwords do not match")
    ])
    confirm = PasswordField("Confirm Password")

@app.route("/register", methods=('GET', 'POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash("Registration Successful")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=('GET', 'POST'))
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        inppassword = request.form["password"]
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            #Get stored hash
            data = cur.fetchone()
            password = data["password"]
            #Compare pass
            if sha256_crypt.verify(inppassword, password):
                app.logger.info("PASSWORD MATCHED")
                session["logged_in"] = True
                flash("You have been logged in!")
                return redirect(url_for("profile", user="admin"))
        else:
            app.logger.info("NO USER")
            error = "The account name or password that you have entered is incorrect."
    return render_template('login.html', error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("overview"))

@app.route("/expiration")
@login_required
def expiration():
    return render_template("expiration.html")

@app.route("/expenditure")
@login_required
def expenditure():
    return render_template("expenditure.html")

@app.route("/profile")
@login_required
def user():
    return render_template("profile.html")

@app.route("/profile/<user>")
def profile(user = None):
    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
