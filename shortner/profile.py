from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import GenName
from .models import Link
from . import db

profile = Blueprint('profile', __name__)

@profile.route("/profile")
@login_required
def profile_route():
    # Same as User model
    name = current_user.name
    return render_template("profile.html", name=current_user.name)

@profile.route("/link", methods=["POST"])
@login_required
def link_route():
    #TODO check url is valid
    new_id = GenName.generate()
    url = request.form.get("url")
    print(new_id, url)

    user_id = current_user.id
    new_link = Link(new_link=new_id, link=url, user_id=user_id)

    db.session.add(new_link)
    db.session.commit()

    return redirect(url_for("profile.profile_route"))