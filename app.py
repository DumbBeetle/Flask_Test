from flask import Flask, render_template
import os

app = Flask(__name__)
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))
DEBUG = bool(os.getenv('DEBUG', False))


@app.route('/')
def home_page():
    deploy_date = os.getenv("DEPLOY_DATE", "N/A")
    deploy_time = os.getenv("DEPLOY_TIME", "N/A")
    git_sha = os.getenv("GIT_SHA", "N/A")
    return render_template("index.html", deploy_date=deploy_date, deploy_time=deploy_time, git_sha=git_sha)

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_404.html"), 404

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
