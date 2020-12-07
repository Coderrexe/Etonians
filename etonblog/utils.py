from etonblog import db


def convert_date(current_time, date_posted):
    time_delta = current_time - date_posted

    if time_delta.days >= 365:
        if time_delta.days < 730:
            return "1 year ago"
        else:
            return str(time_delta.days//365) + " years ago"

    if time_delta.days >= 30:
        if time_delta.days < 60:
            return "1 month ago"
        else:
            return str(time_delta.days//30) + " months ago"

    if time_delta.days >= 1:
        if time_delta.days != 1:
            return str(time_delta.days) + " days ago"
        else:
            return "1 day ago"

    if time_delta.seconds >= 3600:
        if time_delta.seconds < 7200:
            return "1 hour ago"
        else:
            return str(time_delta.seconds//3600) + " hours ago"

    if time_delta.seconds >= 60:
        if time_delta.seconds < 120:
            return "1 minute ago"
        else:
            return str(time_delta.seconds//60) + " minutes ago"
        
    return "Just now"
