from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secretkeygoesherewhoooo'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shortner.db'

    db.init_app(app)

    login_manager = LoginManager()
    # if not logged in redirects to login view
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    # user loader for cookie
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    return app
