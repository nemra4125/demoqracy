import datetime
from basehandler import BaseHandler
from google.appengine.api import users
from model import Election
from utils import ProcessParams

class CreateElectionHandler(BaseHandler):
  def post(self):
    if users.get_current_user() is None:
      raise UserWarning("You must be logged in to create a new election.")
    params = ProcessParams(request=self.request,
                           optional_params=["start", "end"],
                           required_params=["title"])
    election = Election(title=params["title"], owner=users.get_current_user())
    if "start" in params:
      election.start = datetime.datetime.fromtimestamp(params["start"])
    if "end" in params:
      election.end = datetime.datetime.fromtimestamp(params["end"])
    election.put()