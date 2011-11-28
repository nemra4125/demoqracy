from basehandler import BaseHandler
from google.appengine.api import channel
from google.appengine.api import users
from model import ChannelToken, Election
from utils import WriteJsonResponse
from webob.exc import HTTPUnauthorized
import random

class GenerateChannelTokenHandler(BaseHandler):
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    current_user = users.get_current_user()
    if election.owner != current_user:
      raise HTTPUnauthorized("You are not the owner of this election.")
    channel_id = "%s:%s" % (current_user.user_id(), random.random())
    ChannelToken(channel_id=channel_id).put()
    WriteJsonResponse(self,
                      dict(channelToken=channel.create_channel(channel_id)))