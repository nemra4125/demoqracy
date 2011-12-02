from basehandler import BaseHandler
from google.appengine.api import users
from model import Election

class IndexHandler(BaseHandler):
  def get(self):
    if users.get_current_user() is not None:
      elections = [dict(id=election.key().id(), title=election.title)
                   for election
                   in Election.GetElections(users.get_current_user())]
    else:
      elections = []
    self.render_template("index.html", elections=elections)