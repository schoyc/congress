import requests
import congress_app.modules.votes as vts
import os

PAGE_ID = "1586021568096378"
ACCESS_TOKEN = os.environ["FB_CONGRESS_ACCESS_TOKEN"]
FB_API = "https://graph.facebook.com/v2.9"
PAGE_POST_ENDPT = "/" + PAGE_ID + "/feed"
MESSAGE_POST_ENDPT = "/me/messages"

def makeDailyVotesPost(votes, legislator):
    post = votesBlurb(votes, legislator)

    # 2) Target post to only those in district/state
    targeting = {}
    geo_locations = {}
    regions = [{"key" : legislator.districtKey()}]

    geo_locations["regions"] = regions
    targeting["geo_locations"] = geo_locations

    targeting = str(targeting).replace(" ", "")

    # 3) Build request to post to feed (https://developers.facebook.com/docs/graph-api/reference/v2.9/page/feed#publish)
    params = {}
    params["message"] = post
    params["targeting"] = targeting
    params["access_token"] = ACCESS_TOKEN

    response = requests.post(FB_API + PAGE_POST_ENDPT, data=params)

    success = "id" in response.json()
    print(response.json())
    return success

def sendVotesMessage(votes, legislator, user):
    text = votesBlurb(votes, legislator)

    payload = {}

    recipient = {"id" : user}
    message = {"text" : text}
    #TODO: Add links to bills

    payload["recipient"] = recipient
    payload["message"] = message

    response = requests.post(FB_API + MESSAGE_POST_ENDPT, data=payload, params={"access_token" : ACCESS_TOKEN})
    success = "message_id" in response.json()

    return success

def votesBlurb(votes, legislator):
    # 1) Create message for post
    #TODO: Replace legislator name with their FB page
    message = str(legislator) + " just voted:\n"

    # Sort votes into "yea's", "no's", and "not voting"
    # print("VOTES:")
    # print(votes)
    yes_votes, no_votes, abstentions = vts.votesByType(votes)

    headers_to_votes = [
        ("YES on\n", yes_votes),
        ("NO on\n", no_votes),
        ("ABSTAINED from voting on\n", abstentions)
    ]

    for header, votes in headers_to_votes:
        message += header
        for vote in votes:
            bill = vote["bill"]
            title = bill["short_title"]
            if title == None:
                title = bill["official_title"]
            message += title + "\n"
        message += "\n"

    return message
