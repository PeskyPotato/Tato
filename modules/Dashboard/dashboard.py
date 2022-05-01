from flask import Blueprint, render_template, current_app, redirect, abort
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
    if not link:
        abort(404)
    return redirect(link[1])
