from flask import Flask, render_template
import os

from modules.Dashboard.dashboard import dashboard
from modules.API.api import api

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, static_folder="./templates/static")

app.config['SECRET_KEY'] = "24kjt024fh34kf #$JKr3uAO[IH"
app.config['BASE_URL'] = 'http://172.17.137.25:5000/'
app.config['DB_LOCATION'] = os.path.join(
    app.root_path, "links.db"
)
app.config["DEBUG"] = True

app.register_blueprint(dashboard)
app.register_blueprint(api, url_prefix="/api")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="172.17.137.25", debug=True)
