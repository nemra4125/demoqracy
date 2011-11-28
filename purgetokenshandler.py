from basehandler import BaseHandler
from google.appengine.ext import db
from model import ChannelToken
from webapp2_extras.appengine.users import admin_required

class PurgeTokensHandler(BaseHandler):
  @admin_required
  def get(self):
    db.delete(ChannelToken.GetExpiredChannelTokens())