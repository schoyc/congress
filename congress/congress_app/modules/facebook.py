import requests
import congress_app.modules.votes as vts

PAGE_ID = "1586021568096378"
ACCESS_TOKEN = "EAACHhwdFok0BAG4LyqnUp3Q5Hl2AHHTwrHRSWMEb2DUBZCjZA8i1C1ql1eMYM7YvOwj7y5Vg9OanhM9sYXTPOJVa4jZAlu8POzweC4tmZAWzr0fBCGw8jlydB325jPQwwv6WhpzVXLFHvWtaVhXrzpgRxF1JX83JZB9iI1yXdmGwFHYuaBWT5"
FB_API = "https://graph.facebook.com/v2.9"
PAGE_POST_ENDPT = "/" + PAGE_ID + "/feed"

def makeDailyVotesPost(votes, legislator):
    # 1) Create message for post
    #TODO: Replace legislator name with their FB page
    message = str(legislator) + " just voted:\n"

    # Sort votes into "yea's", "no's", and "not voting"
    # print("VOTES:")
    # print(votes)
    yes_votes, no_votes, abstentions = vts.votesByType(votes)

    headers_to_votes = {
        "YES on\n" : yes_votes,
        "NO on\n" : no_votes,
        "ABSTAINED from voting on\n" : abstentions
    }

    for header, votes in headers_to_votes.items():
        message += header
        for vote in votes:
            bill = vote["bill"]
            title = bill["short_title"]
            if title == None:
                title = bill["official_title"]
            message += title + "\n"
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

    response = requests.post(FB_API + PAGE_POST_ENDPT, data=params)

    success = "id" in response.json()
    print(response.json())
    return success
