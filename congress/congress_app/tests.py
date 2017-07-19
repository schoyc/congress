from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client

from .models import Legislator, Representative, Senator
import datetime

# Create your tests here.
class PublishVotesTestCase(TestCase):

    def test_votes_published_for_one_rep(self):
        rep = Representative(first_name="Eric", last_name="Swalwell", state="CA", bioguide_id="S001193", last_vote_time=datetime.datetime(year=2017, month=7, day=6, hour=0, minute=0), district=15)
        rep.save()

        c = Client()
        response = c.post('/congress/publish_votes/posts', {'reps' : 'S001193'})
        print("Response type:" + str(type(response)))
        self.assertIs(len(response.json()['reps']) == 0, True)
