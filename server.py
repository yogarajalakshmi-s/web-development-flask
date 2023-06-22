from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

blogs = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391").json()
blog_objects = []
for blog in blogs:
    blog_obj = Post(blog["id"], blog["title"], blog["subtitle"], blog["body"])
    blog_objects.append(blog_obj)


@app.route('/')
def home():
    return render_template("index.html", blogs=blog_objects)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in blog_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)  # Debug mode on
