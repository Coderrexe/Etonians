from etonians import db
from etonians.models import Upvote


def upvote_post(user_id, post_id):
    upvote = Upvote(user_id=user_id, post_id=post_id)
    db.session.add(upvote)
    db.session.commit()
