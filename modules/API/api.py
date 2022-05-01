from flask import (
    Blueprint, redirect, request, url_for, flash,
    current_app
)
import re
import string
import random
from modules.API.database import Database

api = Blueprint('api', __name__)


@api.route("/link/create", methods=["POST"])
def link_create():
    url = request.form.get("url")
    if not valid_url(url):
        flash("Sorry, invalid URL.", "error")
        return redirect(url_for("dashboard.dashboard_view"))

    new_id = generate_id()

    db = Database(current_app.config["DB_LOCATION"])
    db.insert_link(url, new_id)
    flash(f"Your new link is {current_app.config['BASE_URL']}{new_id}")
    return redirect(url_for("dashboard.dashboard_view"))


def valid_url(url):
    # from django
    url_pattern = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, url)


def generate_id():
    return ''.join(random.choice(
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits) for _ in range(6)
    )
