from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

@app.route("/")
def home():

    return render_template("index.html")


def start_gui():

    app.run(

        debug=False,

        host="127.0.0.1",

        port=5000
    )