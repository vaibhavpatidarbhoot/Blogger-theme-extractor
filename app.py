from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_and_convert(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "My Blogger Template"
        content = str(soup.find('body'))  # Extract body content

        # Blogger XML Template Format
        blogger_template = f"""
        <?xml version='1.0' encoding='UTF-8' ?>
        <b:skin><![CDATA[
        {soup.find('style').string if soup.find('style') else ''}
        ]]></b:skin>
        <b:template-skin>
            <b:section id='header' name='Header'>{title}</b:section>
            <b:section id='main' name='Main'>{content}</b:section>
            <b:section id='footer' name='Footer'>Footer Content</b:section>
        </b:template-skin>
        """

        # Save to file
        with open("blogger_template.xml", "w", encoding="utf-8") as file:
            file.write(blogger_template)

        return "blogger_template.xml"

    except Exception as e:
        return str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        blog_url = request.form["blog_url"]
        xml_file = fetch_and_convert(blog_url)
        return send_file(xml_file, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
