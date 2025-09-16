import os
import requests
import webbrowser

html_url = "https://itakea.github.io/e24_swa/py_intro_3.html"
css_url = "https://itakea.github.io/e24_swa/_static/css/custom.css?v=a5898925"

folder = "MakeMappe"
os.makedirs(folder, exist_ok=True)

html_text = requests.get(html_url).text
html_path = os.path.join(folder, "index.html")

css_text = requests.get(css_url).text
css_name = "custom.css"
css_path = os.path.join(folder, css_name)
with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_text)

html_text = html_text.replace(css_url, css_name)
html_text = html_text.replace("_static/css/custom.css?v=a5898925", css_name)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_text)

webbrowser.open("file://" + os.path.abspath(html_path))
