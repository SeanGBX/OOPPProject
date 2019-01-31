from flask import Flask, render_template, redirect, url_for, request, session, flash, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from currentfood import CurrentFood
from profile import Profile
from allowance import Allowance
import pygal
import time
from pygal.style import Style

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

#wraps wraps up the function into an @
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
@login_required
def overview():
    #retreive allowance
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM allowance")
    allowancedata = cur.fetchall()
    allowance = float(allowancedata[0]["weekly"])
    app.logger.info(allowance)
    cur.close()
    cur = mysql.connection.cursor()
    #Retrieve total price
    cur.execute("SELECT SUM(price) FROM currentfoodlist")
    totaldata = cur.fetchall()
    totaldata2 = totaldata[0]["SUM(price)"]
    if totaldata2 == None:
        totalspent = 0
    else:
        totalspent = round(float(totaldata2),2)
    cur.close()
    #Retrieve total cals
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(calories) FROM currentfoodlist")
    caldata = cur.fetchall()
    totalcal = caldata[0]["SUM(calories)"]
    if totalcal == None:
        totalcal = 0
    else:
        totalcal = int(totalcal)
    daily  = round(allowance / 7, 2)
    weekly = round(allowance, 2)
    monthly = round(allowance * 4, 2)
    custom_style = Style(
        background="transparent",
        plot_background="#FFFFFF",
        foreground="#FFFFFF"
    )
    #Daily Food Expenditure Pie Chart
    pie_chart = pygal.Pie(style=custom_style)
    pie_chart.show_legend = False
    pie_chart.title = "Food Expenditure"
    pie_chart.add({
        "title" : "Allowance left",
    },[{
        "value": daily - totalspent ,
        "xlink" : {"href": "/expenditure", "target":"_parent"}
    }])
    pie_chart.add({
        "title": "Spent",
    }, [{
        "value": totalspent,
        "xlink": {"href": "/expenditure", "target":"_parent"}
    }])
    pie_chart.render_to_file("static/img/chart.svg")
    img_url1 = 'static/img/chart.svg?cache=' + str(time.time())
    #Weekly Food Expenditure Pie Chart
    pie_chart = pygal.Pie(style=custom_style)
    pie_chart.show_legend = False
    pie_chart.title = "Food Expenditure"
    pie_chart.add({
        "title": "Allowance left",
    }, [{
        "value": weekly,
        "xlink": {"href": "/expenditure", "target": "_parent"}
    }])
    pie_chart.add({
        "title": "Spent",
    }, [{
        "value": totalspent,
        "xlink": {"href": "/expenditure", "target": "_parent"}
    }])
    pie_chart.render_to_file("static/img/chart2.svg")
    img_url2 = 'static/img/chart2.svg?cache=' + str(time.time())
    #Monthly Food Expenditure Pie Chart
    pie_chart = pygal.Pie(style=custom_style)
    pie_chart.show_legend = False
    pie_chart.title = "Food Expenditure"
    pie_chart.add({
        "title" : "Allowance left",
    },[{
        "value": monthly - totalspent,
        "xlink" : {"href": "/expenditure", "target":"_parent"}
    }])
    pie_chart.add({
        "title": "Spent",
    }, [{
        "value": totalspent,
        "xlink": {"href": "/expenditure", "target":"_parent"}
    }])
    pie_chart.render_to_file("static/img/chart3.svg")
    img_url3 = 'static/img/chart3.svg?cache=' + str(time.time())
    #Calorie Intake Pie Chart
    pie_chart2 = pygal.Pie(style=custom_style)
    pie_chart2.show_legend = False
    pie_chart2.title = "Caloric Intake"
    pie_chart2.add({
        "title": "Calories",
    }, [{
        "value": totalcal,
        "xlink": {"href": "/expiration", "target":"_parent"}

    }])
    pie_chart2.render_to_file("static/img/chartcal.svg")
    img_url4 = 'static/img/chartcal.svg?cache=' + str(time.time())
    return render_template("overview.html", img_url1=img_url1, img_url2=img_url2, img_url3=img_url3, img_url4=img_url4)

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
            # Get stored hash
            data = cur.fetchone()
            password = data["password"]
            # Get user info
            name = data["name"]
            email = data["email"]
            id = data["id"]
            #Compare pass
            if sha256_crypt.verify(inppassword, password):
                app.logger.info("PASSWORD MATCHED")
                session["logged_in"] = True
                session["username"] = username
                session["name"] = name
                session["email"] = email
                session["allowance"] = 0
                session["id"] = id
                return redirect(url_for("profile", user=username))
        else:
            app.logger.info("ERROR OCCURRED")
            error = "The account name or password that you have entered is incorrect."
    return render_template('login.html', error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))

class AddItemForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    time = StringField("Time", [validators.Length(min=1, max=365)])

@app.route("/expiration", methods=('GET', 'POST'))
@login_required
def expiration():
    session["url"] = "expiration"
    form = AddItemForm(request.form)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    foodexp = cur.fetchall()
    cur.close()
    if request.method == "POST":
        delitem = request.form.get("delfood")
        edititem = request.form.get("editfood")
        app.logger.info(delitem)
        if delitem:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM items WHERE id = %s", [delitem])
            cur.execute("ALTER TABLE items AUTO_INCREMENT = 1")
        elif edititem:
            app.logger.info(edititem)
            return redirect(url_for("setexpiration",edititem=edititem))
        else:
            pass
        return redirect(url_for("expiration"))
    """
    name = form.name.data
        time = form.time.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO items(name, expiry) Values(%s, %s)", (name, time))
        mysql.connection.commit()
        cur.close()
    """
    # for i in y:
    # time = i.expiry
    # stop_time = datetime.datetime.now() + datetime.timedelta(hours = time * 24)
    # if datetime.datetime.now() > stop_time:
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO items(status = '1')")
    # mysql.connection.commit()
    # cur.close()
    # cur = mysql.connection.cursor()
    # cur.execute("Delete from items where status='1'")
    # mysql.connection.commit()
    # cur.close()

    return render_template("expiration.html", form=form, foodexp=foodexp)

@app.route("/setexpiration", methods=('GET', 'POST'))
@login_required
def setexpiration():
    form = AddItemForm(request.form)
    if request.method == "POST":
        edititem = request.args["edititem"]
        name = form.name.data
        time = form.time.data
        app.logger.info(edititem)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE items SET expiry=%s, name=%s WHERE id =%s", (time,name, edititem) )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("expiration"))
    return render_template("setExpiry.html", form=form)
@app.route("/expenditure", methods=('GET', 'POST'))
@login_required
def expenditure():
    session["url"] = "expenditure"
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM currentfoodlist")
    data2 = cur.fetchall()
    cur.execute("SELECT SUM(price) FROM currentfoodlist")
    totaldata = cur.fetchall()
    totaldata2 = totaldata[0]["SUM(price)"]
    if totaldata2 == None:
        totalspent = 0
    else:
        totalspent = float(totaldata2)

    cur.close()
    # get from db and display Allowance
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM allowance")
    allowance = cur.fetchall()
    weekly = float(allowance[0]['weekly'])
    cur.close()
    app.logger.info(weekly)
    totalexpenditure = weekly - totalspent
    if request.method == "POST":
        fooditem = request.form["delfood"]
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM currentfoodlist WHERE id = %s", [fooditem])
        cur.execute("ALTER TABLE currentfoodlist AUTO_INCREMENT = 1")
        app.logger.info(fooditem)
        return redirect(url_for("expenditure"))

    return render_template("expenditure.html", data2=data2, weekly=weekly, totalspent=totalspent, totalexpenditure=totalexpenditure)

@app.route("/allowance", methods=('GET', 'POST'))
@login_required
def editAllowance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM allowance")
    allowance = cur.fetchall()
    weekly = float(allowance[0]['weekly'])
    cur.close()
    if request.method == "POST":
        editallowance = request.form["allowance"]
        #create object with new values
        new = Allowance(editallowance)
        new.changeAllowance()
        app.logger.info(editallowance)
        return redirect("expenditure")

    return render_template("allowance.html", weekly=weekly)

@app.route("/addfood", methods=('GET', 'POST'))
@login_required
def addfood():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM foodlist")
    data = cur.fetchall()
    cur.close()
    if request.method == "POST":
        foodrow = request.form["addfood"]
        mylist = foodrow.split(",")
        app.logger.info(mylist)
        food = mylist[0]
        price = mylist[1]
        calories = mylist[2]
        foodinfo = CurrentFood(food, price, calories)
        foodinfo.insert_food()
        app.logger.info(foodinfo)
        if "url" in session:
            return redirect(url_for(session["url"]))
        return redirect(url_for("overview"))

    return render_template("addfood.html", data=data)

@app.route("/profile/")
@login_required
def user():
    username = session["username"]
    return redirect(url_for("profile", user=username))

@app.route("/profile/<user>")
@login_required
def profile(user):
    # match user data row with session id
    sesID = session["id"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [sesID])
    profilelist = cur.fetchone()
    name = profilelist['name']
    username = profilelist['username']
    email = profilelist['email']

    return render_template("profile.html",user=user, name=name, username=username, email=email)

@app.route("/profile/editprofile", methods=('GET', 'POST'))
@login_required
def editprofile():
    # get new values from form
    sesID = session["id"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [sesID])
    profilelist = cur.fetchone()
    name = profilelist['name']
    username = profilelist['username']
    email = profilelist['email']
    if request.method == "POST":
        editname = request.form["name"]
        editusername = request.form["username"]
        editemail = request.form["email"]
        editID = session["id"]
        # new values saved in db
        new = Profile(editname, editusername, editemail, editID)
        new.changeProfile()
        session["username"] = editusername
        return redirect(url_for("user"))
    else:
        app.logger.info("Form Error")

    return render_template("editprofile.html",user=user, name=name, username=username, email=email)


if __name__ == "__main__":
    app.run(debug=True, port="80")
