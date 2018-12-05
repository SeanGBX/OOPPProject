from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def overview():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/expiration")
def expiration():
    return render_template("expiration.html")

@app.route("/expenditure")
def expenditure():
    return render_template("expenditure.html")

@app.route("/profile/<user>")
def index(user = None):
    return render_template("profile.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
