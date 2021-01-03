from elasticsearch import Elasticsearch

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

# configurations
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# if a user tries to go to a page that is @login_required, they will be directed to the login_view, which I set to be the login page
login_manager.login_view = "users.login"
login_manager.login_message = "You must log in first to view this page."
login_manager.login_message_category = "warning"
mail = Mail()
admin = Admin()
migrate = Migrate(compare_type=True)

from etonians.models import *


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db=db, render_as_batch=True)

    if app.config["ELASTICSEARCH_URL"]:
        app.elasticsearch = Elasticsearch([app.config["ELASTICSEARCH_URL"]])

    from etonians.users.views import users
    from etonians.posts.views import posts
    from etonians.main.views import main
    from etonians.comments.views import comments
    from etonians.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(comments)
    app.register_blueprint(errors)

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(EmailVerificationCode, db.session))
    admin.add_view(ModelView(TemporaryUser, db.session))

    return app
