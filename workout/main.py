from flask import Flask, render_template, url_for


app = Flask(import_name=__name__, static_folder=r"C:\Users\ПК\Desktop\SQLite\workout")

@app.route("/")
def hundler():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
