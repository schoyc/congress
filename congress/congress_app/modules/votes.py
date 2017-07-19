import requests
import datetime
from congress_app.modules.util import *

SUNLIGHT_API = "https://congress.api.sunlightfoundation.com"
VOTES = SUNLIGHT_API + "/votes"

def getBillVotes(legislator_id, until=None):
    voter_id = "voter_ids." + str(legislator_id)
    fields = [voter_id, "roll_type", "question", "voted_at",
                "bill.bill_id", "bill.official_title", "bill.short_title",
                "bill.popular_title"
    ]

    params = {
        "vote_type" : "passage",
        "order" : "voted_at",
        "fields" : ",".join(fields)
    }

    response = requests.get(VOTES, params)
    print("URL: " + str(response.url))
    response = response.json()

    results = response["results"]
    results_count = response["count"]
    results_page = response["page"]

    if until == None:
        until = toDatetime(results[-1]["voted_at"])

    votes = []

    i = 0
    vote_time = toDatetime(results[i]["voted_at"])
    while vote_time > until and i < results_count:
        result = results[i]
        votes.append(result)
        i += 1
        vote_time = toDatetime(results[i]["voted_at"])

        # TODO: Handle i > results_count, unlikely that
        # more than 20 votes per day, but for robustness

    return votes

# TODO: Implement
def votesByType(votes):
    yes_s, no_s, abstentions = [], [], []
    for vote in votes:
        try:
            vote_type = list(vote["voter_ids"].values())[0]
            if vote_type == "Yea":
                yes_s.append(vote)
            elif vote_type == "Nay":
                no_s.append(vote)
            else:
                abstentions.append(vote)
        except IndexError:
            print("BAD VOTE" + str(vote["voter_ids"]))

    return yes_s, no_s, abstentions
