from basehandler import BaseHandler
from utils import ProcessParams
from model import Election
from google.appengine.api import users
import datetime

class CreateElectionHandler(BaseHandler):
  def post(self):
    if users.get_current_user() is None:
      raise UserWarning("You must be logged in to create a new election.")

    params = ProcessParams(request=self.request,
                           optional_params=["start", "end"],
                           required_params=["title"])

    election = Election(title=params["title"], owner=users.get_current_user())
    if "start" in params:
      pass
    election.put()