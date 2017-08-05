from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^publish_votes/posts$', views.publishDailyVotes, name="daily_vote_posts"),
    url(r'^messenger-bot$', views.messengerBot, name="messenger_bot")
]
