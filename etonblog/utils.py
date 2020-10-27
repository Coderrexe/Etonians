def convert_date(current_time, date_posted):
    split_by_comma = str(current_time - date_posted).split(",")
    split_by_colon = str(current_time - date_posted).split(":")

    if len(split_by_comma) > 1:
        return split_by_comma[0] + " ago"
    else:
        if int(split_by_colon[0]) > 0:
            if split_by_colon[0] != "1":
                return split_by_colon[0] + " hours ago"
            else:
                return "1 hour ago"
        else:
            if int(split_by_colon[1]) > 0:
                if int(split_by_colon[1]) < 10:
                    minutes = int(split_by_colon[1])
                    if minutes == 1:
                        return "1 minute ago"
                    else:
                        return str(minutes) + " minutes ago"
                else:
                    return split_by_colon[1] + " minutes ago"
            else:
                return "Just now"
