from etonblog import db


def convert_date(current_time, date_posted):
    time_delta = current_time - date_posted

    if time_delta.days > 0:
        if time_delta.days != 1:
            return str(time_delta.days) + " days ago"
        else:
            return "1 day ago"

    if time_delta.seconds > 3600:
        return str(time_delta.seconds//3600) + " hours ago"

    if time_delta.seconds > 119:
        return str(time_delta.seconds//60) + " minutes ago"

    if time_delta.seconds > 59:
        return str(time_delta.seconds//60) + " minute ago"
        
    return "Just now"
