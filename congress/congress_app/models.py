from django.db import models

# Create your models here.
class Legislator(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=2)

    bioguide_id = models.CharField(max_length=10, default='0000000000')
    last_vote_time = models.DateTimeField()

    class Meta:
        abstract = True

class Representative(Legislator):
    district = models.PositiveIntegerField()

    def districtKey(self):
        return "US:" + self.state + "%02d" % district

class Senator(Legislator):
    election_year = models.DateField()
    stateRegionKey = models.PositiveIntegerField()

    def districtKey(self):
        return stateRegionKey
