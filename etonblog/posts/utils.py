from etonblog import db
from etonblog.models import Upvote


def like_post(author, post):
    upvote = Upvote(author=author, post=post)
    db.session.add(upvote)
    db.session.commit()
