from basehandler import BaseHandler
from channelapihelper import ChannelApiHelper
from model import Election
from utils import WriteJsonResponse

class GenerateChannelTokenHandler(BaseHandler):
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    channel_token = ChannelApiHelper(election).CreateChannel()
    WriteJsonResponse(self, dict(channelToken=channel_token))