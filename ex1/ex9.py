import os
from unicodedata import category
from flask import Flask, flash, render_template, url_for, \
    request


# Configuration
DATABASE = "./database/urls.db"
SECRET_KEY = "asdkfj4893aa32lma;31"
DEBUG = True

app = Flask(import_name=__name__)
app.config.from_object(__name__)

@app.route("/")
def main_handler():
    # db = get_db()
    # dbase = FDataBase(db)
    return render_template("index.html", title="Flsite", current=os.path.basename(os.getcwd()))

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if request.form["username"] != "Ahmat":
            print("request: ", request.form["username"])
            flash("Сообщение было отправлено, без кипишей", category="success")
        else:
            flash("ошибка сообщения", category="error")
    return render_template("content.html", title="Help")


if __name__ == "__main__":
    app.run(debug=True)
