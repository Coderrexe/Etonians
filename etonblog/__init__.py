from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from etonblog.config import Config

# configurations
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# if a user tries to go to a page that is @login_required, they will be directed to the login_view, which I set to be the login page
login_manager.login_view = "users.login"
login_manager.login_message_category = "info" # this sets the flash message "Please login to view this page" to be light blue
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import at the end of program in order to avoid circular import
    # "users", "posts" and "main" are Blueprint variables
    from etonblog.users.routes import users
    from etonblog.posts.routes import posts
    from etonblog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
