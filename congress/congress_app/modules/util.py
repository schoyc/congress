import datetime

def toDatetime(timestring):
    return datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
