from flask import Flask, render_template, request, flash, session, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "alexey"


@app.route("/")
def main():
    return "<h1>Here: <a href=http://127.0.0.1:5000/contact> link </a> </h1>"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if request.form["username"] == "Alexey":
            flash("Сообщение отправлено", category="success")
        else:
            flash("Сообщение не отправлено", category="error")
            return redirect(url_for("nahui", username=request.form["username"]))
    return render_template("content.html", title="About Flask")


@app.route("/nahui/<username>")
def nahui(username):
    return f"Poshel v zhopy {username})"


if __name__ == "__main__":
    app.run(debug=True)
