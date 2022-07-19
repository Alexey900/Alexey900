from flask import Flask, render_template, url_for, session, redirect

app = Flask(__name__)
template_path = "index.html"

tags = ["Just", "Breake", "every", "day", "say"]


@app.route("/")
def handler():
    print("url -> ", url_for("handler"))
    return render_template(template_path, name="Flask", tags=tags)


@app.route("/about/<path:username>")
def about_(username):
    return render_template("about.html") + "username: " + username


if __name__ == "__main__":
    app.run(debug=True)
