from django.shortcuts import render
from django.http import HttpResponse

import requests
import util

SUNLIGHT_API = "https://congress.api.sunlightfoundation.com"
VOTES = SUNLIGHT_API + "/votes"

# Create your views here.

def getVotesForLegislator(request, legislator_id):
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

    return HttpResponse(results)

def updateVotes(request):

    for legislator in legislators:
        # make API call to /votes
        params = {"voter_ids." + legislator_id + "__exists" : "true"}
        response = requests.get(VOTES, params)

        response = response.json()
        results = response["results"]

        # TODO: Get time of most recent vote by legislator
        last_vote_time = None

        # Find all votes since that time
        for vote in results:
            vote_time = util.toDatetime(vote["voted_at"])
            if vote_time > last_vote_time:
                # TODO: save vote in database
            else:
                break
