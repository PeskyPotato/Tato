from flask import (
    Blueprint, render_template, current_app, redirect, abort, request
)
from datetime import datetime
from modules.API.database import Database

dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/")
def dashboard_view():
    db = Database(current_app.config["DB_LOCATION"])
    links = db.select_links()
    print(links)
    return render_template("dashboard.html", links=links)


@dashboard.route("/s/<link_id>")
def link_redirect(link_id):
    db = Database(current_app.config["DB_LOCATION"])
    link = db.select_link(link_id)

    ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    if ip is None:
        ip = request.environ.get('REMOTE_ADDR')
    db.insert_stat(int(datetime.now().timestamp()), ip, link_id)

    if not link:
        abort(404)
    return redirect(link[1])
