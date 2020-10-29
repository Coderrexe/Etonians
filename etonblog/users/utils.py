import os
import secrets
import random
from PIL import Image
from flask import url_for
from flask_mail import Message
from flask_login import current_user

from etonblog import app, db, mail
from etonblog.models import EmailVerificationCode


def save_picture(form_picture):
    # picture files will be turned into random_hexes in order to prevent pictures of the same name
    random_hex = secrets.token_hex(8) 
    _, file_extension = os.path.splitext(form_picture.filename) # "_" is used for throwaway variables
    picture_file_name = random_hex + file_extension
    # stores the picture to the profile_pictures folder
    picture_path = os.path.join(app.root_path, "static", "profile_pictures", picture_file_name)

    # resize the profile picture to 200 pixels by 200 pixels
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    old_picture = os.path.join(app.root_path, "static", "profile_pictures", current_user.image_file)
    if os.path.exists(old_picture) and old_picture != os.path.join(app.root_path, "static", "profile_pictures", "default.jpg"):
        os.remove(old_picture)

    return picture_file_name


# this function is called in reset_request route, and sends an email to the user
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender="noreply@etonians.co.uk", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
    
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
"""
    mail.send(msg)


def send_verify_email(user_email):
    verification_code = random.randrange(100000, 999999)
    verification_code_list = EmailVerificationCode.query.all()

    while verification_code in verification_code_list:
        verification_code = random.randrange(100000, 999999)

    db.session.add(verification_code)
    db.session.commit()

    msg = Message("Verify your email", sender="noreply@etonians.co.uk", recipients=[user_email])
    msg.body = f"{verification_code}"

    mail.send(msg)
