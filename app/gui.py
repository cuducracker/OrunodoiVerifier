from flask import Flask, render_template
from flask_cors import CORS
from app.routes import register_routes

app = Flask(

    __name__,

    template_folder="../templates",

    static_folder="../static"

)


CORS(app, origins=[
    "https://ank-ldb.blogspot.com"
])
register_routes(app)
@app.route("/")
def home():

    return render_template(

        "index.html"

    )