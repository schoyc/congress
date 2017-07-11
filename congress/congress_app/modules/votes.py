import requests
import datetime

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
        votes.append(result)
        i += 1
        vote_time = toDatetime(results[i]["voted_at"])

        # TODO: Handle i > results_count, unlikely that
        # more than 20 votes per day, but for robustness

    return votes

# TODO: Implement
def votesByType(votes):
    return votes
