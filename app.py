from flask import Flask, render_template, send_from_directory
import os, markdown

app = Flask(__name__)

@app.route("/")
def index():
    posts = sorted(os.listdir("blog/posts"), reverse=True)
    return render_template("index.html", posts=posts)

@app.route("/post/<name>")
def post(name):
    with open(f"blog/posts/{name}", "r") as f:
        content = markdown.markdown(f.read())
    return render_template("post.html", content=content)

@app.route("/static/img/<path:filename>")
def serve_image(filename):
    return send_from_directory("static/img", filename)
