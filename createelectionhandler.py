from basehandler import BaseHandler
from google.appengine.api import users
from model import Candidate, Election
from utils import ProcessParams
from webob.exc import HTTPUnauthorized
import datetime

class CreateElectionHandler(BaseHandler):
  
  def get(self):
    self.render_template("create.html")
  
  def post(self):
    if users.get_current_user() is None:
      raise HTTPUnauthorized("You must be logged in to create a new election.")
    params = ProcessParams(request=self.request,
                           optional_params=["start", "end"],
                           required_params=["title", "candidates"])
    election = Election(title=params["title"], owner=users.get_current_user())
    if "start" in params:
      election.start = datetime.datetime.fromtimestamp(params["start"])
    if "end" in params:
      election.end = datetime.datetime.fromtimestamp(params["end"])
    election.put()
    for name in params["candidates"].split(","):
      candidate = Candidate(parent=election, name=name)
      candidate.put()