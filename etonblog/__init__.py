import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASSWORD")
mail = Mail(app)

# import at the end of program in order to avoid circular import
from etonblog import routes
