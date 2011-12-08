from basehandler import BaseHandler
from channelapihelper import GetExpiredChannels
from google.appengine.ext import db
from webapp2_extras.appengine.users import admin_required

class PurgeTokensHandler(BaseHandler):
  @admin_required
  def get(self):
    db.delete(GetExpiredChannels())