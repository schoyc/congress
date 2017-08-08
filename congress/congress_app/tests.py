from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client

from .models import Legislator, Representative, Senator
import datetime
import os

import congress_app.modules.google as google

# Create your tests here.
class PublishVotesTestCase(TestCase):

    def test_votes_published_for_one_rep(self):
        rep = Representative(first_name="Eric", last_name="Swalwell", state="CA", bioguide_id="S001193", last_vote_time=datetime.datetime(year=2017, month=7, day=6, hour=0, minute=0), district=15)
        rep.save()

        c = Client()
        response = c.post('/congress/publish_votes/posts', {'reps' : 'S001193', 'sens' : ''})
        print("Response type:" + str(type(response)))
        self.assertIs(len(response.json()['reps']) == 0, True)

    def test_messenger_verify(self):
        c = Client()
        response = c.get('/congress/messenger-bot', {'hub.mode' : 'subscribe', 'hub.challenge' : '123456', 'hub.verify_token' : os.environ['FB_VERIFY_TOKEN']})

        self.assertIs(response.status_code == 200, True)

class GoogleCallsTestCase(TestCase):

    def test_address_to_districts(self):
        state, district = google.addressToDistricts("1 Hacker Way, Menlo Park, CA")
        self.assertIs(state == 'CA', True)
        self.assertIs(district == '14', True)
