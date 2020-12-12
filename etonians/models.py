from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

from etonians import app, db, login_manager


# user_loader function which returns a user with a certain ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# SQLAlchemy models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    year_group = db.Column(db.String(1), nullable=False)
    # backref allows "author" attribute to be accessed when displaying info about a post
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    upvotes = db.relationship("Upvote", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("UTF-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.year_group}')"


class TemporaryUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    year_group = db.Column(db.String(1), nullable=False)


class EmailVerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Integer, nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    year_group = db.Column(db.String(1), nullable=False)
    filter_year_group = db.Column(db.String(5), nullable=False)
    # sets up a reference with posts (variable defined in class User)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="post", lazy=True)
    upvotes = db.relationship("Upvote", backref="post", lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.year_group}', '{self.filter_year_group}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __repr__(self):
        return f"Comment('{self.title}', '{self.date_posted}')"


class Upvote(db.Model):
    # one user cannot upvote a post twice so user_id, post_id together appear uniquely in this table
    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Upvote('{self.post_id}', '{self.user_id}')"