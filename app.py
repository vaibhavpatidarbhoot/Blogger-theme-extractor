from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        blog_url = request.form["blog_url"]
        return f"You entered: {blog_url}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
