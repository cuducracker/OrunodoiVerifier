from flask import Flask, render_template

from app.routes import register_routes

app = Flask(

    __name__,

    template_folder="../templates",

    static_folder="../static"

)

register_routes(app)


@app.route("/")
def home():

    return render_template(

        "index.html"

    )