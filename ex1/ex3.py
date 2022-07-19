from flask import Flask, abort, redirect, url_for

app = Flask(__name__)

@app.route("/<path>")
def index(path):
    return "hello world"


if __name__ == "__main__":
    app.run(debug=True)
