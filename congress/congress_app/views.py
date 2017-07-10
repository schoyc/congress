from django.shortcuts import render
from .models import Legislator, Representative, Senator
from django.http import HttpResponse
from django.http import JsonResponse

import requests
import util
import votes as vts
import facebook as fb

SUNLIGHT_API = "https://congress.api.sunlightfoundation.com"
VOTES = SUNLIGHT_API + "/votes"

# Create your views here.

def publishDailyVotes(request):
    # Get most recent votes for each legislator

    # For each legislator:
    # 1) Match legislator to city / zipcode
    # 2) Publish votes to Facebook page feed.

    representatives = []
    senators = []

    if 'reps' in request.POST:
        legislators = request.POST['reps'].split(",")
    else:
        representatives = Representative.objects.all()

    if 'sens' in request.POST:
        legislators = request.POST['sens'].split(",")
    else:
        senators = Senator.objects.all()

    response = {}
    # Representatives first
    error_reps = []
    for rep in representatives:
        rep_id = rep.bioguide_id
        votes = vts.getBillVotes(rep_id)

        success = fb.makeDailyVotesPost(votes, rep)
        if not success:
            error_reps.append(rep_id)

    # Senators next
    error_senators = []
    for senator in senators:
        sen_id = senator.bioguide_id
        votes = vts.getBillVotes(sen_id)

        success = fb.makeDailyVotesPost(votes, senator)
        if not success:
            error_senators.append(sen_id)

    response["reps"] = ",".join(error_reps)
    response["sens"] = ",".join(error_senators)

    return JsonResponse(response)

def getVotesForLegislator(request, legislator_id):
    results = vts.getBillVotes(legislator_id)

    return HttpResponse(results)

def updateVotes(request):
    for legislator in legislators:
        # make API call to /votes
        params = {"voter_ids." + legislator_id + "__exists" : "true"}
        response = requests.get(VOTES, params)

        response = response.json()
        results = response["results"]

        last_vote_time = legislator.last_vote_time

        # Find all votes since that time
        for vote in results:
            vote_time = util.toDatetime(vote["voted_at"])
            if vote_time > last_vote_time:
                # TODO: save vote in database
            else:
                break
