from basehandler import BaseHandler
from channelapihelper import ChannelApiHelper
from google.appengine.api import users
from model import Election
from utils import WriteJsonResponse
from webob.exc import HTTPUnauthorized

class GenerateChannelTokenHandler(BaseHandler):
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    current_user = users.get_current_user()
    if not election.public_results and election.owner != current_user:
      raise HTTPUnauthorized("You are not the owner of this election.")
    channel_token = ChannelApiHelper(election).CreateChannel()
    WriteJsonResponse(self,
                      dict(channelToken=channel_token))