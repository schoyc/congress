import requests
import congress_app.modules.votes as vts

PAGE_ID = ""
ACCESS_TOKEN = ""
FB_API = "https://graph.facebook.com/v2.9"
PAGE_POST_ENDPT = "/" + PAGE_ID + "/feed"

def makeDailyVotesPost(votes, legislator):
    # 1) Create message for post
    #TODO: Replace legislator name with their FB page
    message = str(legislator) + " just voted:\n"

    # Sort votes into "yea's", "no's", and "not voting"
    yes_votes, no_votes, abstentions = vts.votesByType(votes)

    message += "YES on\n"
    for vote in yes_votes:
        message += vote["bill"]["short_title"]
    message += "\n"

    message += "NO on\n"
    for vote in no_votes:
        message += vote["bill"]["short_title"]
    message += "\n"

    message += "ABSTAINED from voting on\n"
    for vote in abstentions:
        message += vote["bill"]["short_title"]
    message += "\n"

    # 2) Target post to only those in district/state
    targeting = {}
    geo_locations = {}
    regions = [{"key" : legislator.districtKey()}]

    geo_locations["regions"] = regions
    targeting["geo_locations"] = geo_locations

    targeting = str(targeting).replace(" ", "")

    # 3) Build request to post to feed (https://developers.facebook.com/docs/graph-api/reference/v2.9/page/feed#publish)
    params = {}
    params["message"] = message
    params["targeting"] = targeting
    params["access_token"] = ACCESS_TOKEN

    response = request.post(PAGE_POST_ENDPT, data=params)

    success = "id" in response.json()

    return success
