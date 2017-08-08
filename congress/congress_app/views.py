from django.shortcuts import render
from .models import Legislator, Representative, Senator
from django.http import HttpResponse
from django.http import JsonResponse

import requests
import os

import congress_app.modules.util
import congress_app.modules.votes as vts
import congress_app.modules.facebook as fb
import congress_app.modules.messenger as messenger

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
        reps = request.POST['reps']
        if reps != '':
            for rep_id in reps.split(","):
                print("ID", rep_id)
                representatives.append(Representative.objects.get(bioguide_id=rep_id))
    else:
        representatives = Representative.objects.all()

    if 'sens' in request.POST:
        sens = request.POST['sens']
        if sens != '':
            for sen_id in sens.split(","):
                senators.append(Senator.objects.get(bioguide_id=sen_id))
    else:
        senators = Senator.objects.all()

    response = {}
    # Representatives first
    error_reps = []
    for rep in representatives:
        rep_id = rep.bioguide_id
        votes = vts.getBillVotes(rep_id)
        # response["votes"] = votes

        success = fb.makeDailyVotesPost(votes, rep)
        response["success"] = success
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
    print("RESPONSE: " + str(response))

    return JsonResponse(response)

def messengerBot(request):
    if request.method == "GET":
        try:
            if request.GET['hub.mode'] == 'subscribe' and request.GET['hub.verify_token'] == os.environ['FB_VERIFY_TOKEN']:
                return HttpResponse(request.GET['hub.challenge'])
        except KeyError as e:
            print(e)
            response = HttpResponse()
            response.status_code = 400
            return response

    elif request.method == "POST":
        data = request.POST
        if data["object"] == 'page':
            for entry in data["entry"]:
                pageID = entry["id"]
                entryTime = entry["time"]

                for event in entry["messaging"]:
                    messenger.respondToMessageEvent(event)

            # send back success
            return HttpResponse()



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
                continue
            else:
                break
