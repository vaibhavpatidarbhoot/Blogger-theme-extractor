from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_and_convert(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, "Error: Unable to fetch the Blogspot page."

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "My Blogger Template"
        body_content = str(soup.find('body')) if soup.find('body') else "<p>No content found.</p>"
        
        # Blogger XML Template
        blogger_template = f"""<?xml version='1.0' encoding='UTF-8' ?>
        <b:skin><![CDATA[
        {soup.find('style').string if soup.find('style') else ''}
        ]]></b:skin>
        <b:template-skin>
            <b:section id='header' name='Header'>{title}</b:section>
            <b:section id='main' name='Main'>{body_content}</b:section>
            <b:section id='footer' name='Footer'>Footer Content</b:section>
        </b:template-skin>
        """

        xml_filename = "blogger_template.xml"
        with open(xml_filename, "w", encoding="utf-8") as file:
            file.write(blogger_template)

        return xml_filename, None

    except Exception as e:
        return None, str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        blog_url = request.form["blog_url"]
        xml_file, error = fetch_and_convert(blog_url)
        if error:
            return f"<p style='color:red;'>Error: {error}</p>"
        return send_file(xml_file, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
