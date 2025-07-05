from flask import Flask, render_template
import os

app = Flask(__name__)
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', '8080'))
DEBUG = bool(os.getenv('DEBUG', False))


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/about')
def about_page():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_404.html"), 404

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
