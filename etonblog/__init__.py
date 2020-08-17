from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from jinja2 import BaseLoader
from itsdangerous import TimedJSONWebSignatureSerializer

# configurations
app = Flask(__name__)
app.config["SECRET_KEY"] = "095122deb52285f629106036dcf6f8f39c91f17178cd3346130f72f2d86b7607"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
# if a user tries to go to a page that is @login_required, they will be directed to the login_view, which I set to be the login page
login_manager.login_view = "login"
login_manager.login_message_category = "info" # this sets the flash message "Please login to view this page" to be light blue

# import at the end of program in order to avoid circular import
from etonblog import routes
