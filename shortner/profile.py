from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import re
import GenName
from .models import Link, Stats
from . import db

profile = Blueprint('profile', __name__)


@profile.route("/profile")
@login_required
def profile_route():
    # TODO list all user created links
    # TODO display statistics for each link

    links_obj = Link.query.filter_by(user_id=current_user.id).all()
    links = []
    for i in range(len(links_obj)):
        links.append(links_obj[i].__dict__)
        links[i]["clicks"] = Stats.query.filter_by(link_id=links[i]["id"]).count()
    return render_template("profile.html", name=current_user.name, links=links)


@profile.route("/link", methods=["POST"])
@login_required
def link_route():
    url = request.form.get("url")
    if not valid_url(url):
        flash("Sorry, incorrect URL.", "error")
        print("incorrect", url)
        return redirect(url_for("profile.profile_route"))

    # TODO check for duplicates
    new_id = GenName.generate()
    print(new_id, url)

    user_id = current_user.id
    new_link = Link(new_link=new_id, link=url, user_id=user_id)

    db.session.add(new_link)
    db.session.commit()

    flash("Your new link is localhost:5000/s/{}".format(new_id), "success")
    return redirect(url_for("profile.profile_route"))


def valid_url(url):
    # from django
    url_pattern = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, url)
