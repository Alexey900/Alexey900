import sqlite3

import os
from FDataBase import FDataBase
from flask import redirect, render_template, Flask, request, flash, abort


# CONFIGURATION
DATABASE = "posts.db"
SECRET_KEY = "a;df32;klj asdf 2323"
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "posts.db")))
print(app.root_path, os.getcwd())


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.errorhandler(404)
def handle_bad_request(e):
    return '<h1>bad request!</h1>', 400


# menu =   #MUST BE DICLARET 

@app.route("/")
def handler():
    db = connect_db()
    db = FDataBase(db)

    return render_template("index.html", title="FlaskSite", menu=db.getMenu()[::-1])


@app.route("/add_post", methods=["GET", "POST"])
def AddPost():
    if request.method == "POST":
        db = FDataBase(connect_db())
        if db.addContent(request.form) == 200:
            flash("Пост опубликован", category="success")
        else:
            flash("Ошибка", category="error")
    return render_template("add_menu.html")


@app.route("/<int:post_id>")
def showPost(post_id):
    db = FDataBase(connect_db())
    respone = db.getPost(post_id)
    print(post_id, respone)
    if not respone:
        abort(404)

    return render_template("post_skeleton.html", id=respone["id"],
                           content=respone["content"], title=respone["title"])

@app.route("/delete_post<int:post_id>")
def delete_post(post_id):
    db = FDataBase(connect_db())
    db.deletePost(post_id)
    return "<h1>Пост удален</h1><br><a href='/'>Главная страница</a>"


if __name__ == "__main__":
    app.run(debug=True)
