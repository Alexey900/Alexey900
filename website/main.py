from flask import render_template, Flask, url_for, session, abort, redirect, \
                  request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route("/")
def start():
    return "тебе <a href='http://127.0.0.1:5000/login'>сюда</a>"


@app.route('/login', methods=["POST", "GET"])
def handler():
    if "userLogged" in session:
        return redirect(url_for("profile", username=session["userLogged"]))
    elif request.method == "POST" and request.form["username"] == "Akhmat" and request.form["passw"] == "321":
        session["userLogged"] = "Akhmat"
        return redirect(url_for("profile", username=session["userLogged"]))
    return render_template("registration.html", title="Registration")


@app.route("/profile/<username>")
def profile(username):
    if session["userLogged"] != username:
        abort(401)
    return f"<h1>Добро Пожаловать! {username}<h1>"


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
