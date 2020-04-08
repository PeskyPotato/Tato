from flask import Blueprint, render_template, redirect
from .models import Link

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('index.html')


@main.route("/s/<link_id>")
def link_redirect(link_id):
    # TODO sanitize link_id
    link = Link.query.filter_by(new_link=link_id).first()
    return redirect(link)
