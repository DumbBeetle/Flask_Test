from flask import Flask, render_template

app = Flask(__name__)
host = "0.0.0.0"
port = 5000


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
    app.run(debug=True, host=host, port=port)
