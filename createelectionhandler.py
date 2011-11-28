from basehandler import BaseHandler
from google.appengine.api import users
from model import Candidate, Election
from utils import ProcessParams
from webob.exc import HTTPUnauthorized
from webapp2_extras.appengine.users import login_required
import datetime

class CreateElectionHandler(BaseHandler):
  @login_required
  def get(self):
    self.render_template("create.html", render_form=True)
  
  def post(self):
    if users.get_current_user() is None:
      raise HTTPUnauthorized("You must be logged in to create a new election.")
    params = ProcessParams(request=self.request,
                           optional_params=["start_ts", "end_ts"],
                           required_params=["title", "candidates"])
    #TODO: Move this to a transaction.
    election = Election(title=params["title"], owner=users.get_current_user())
    if "start_ts" in params:
      election.start = datetime.datetime.fromtimestamp(params["start_ts"])
    if "end_ts" in params:
      election.end = datetime.datetime.fromtimestamp(params["end_ts"])
    election.put()
    for name in params["candidates"].split("||"):
      candidate = Candidate(parent=election, name=name)
      candidate.put()
      
    self.render_template("create.html",
                         render_form=False,
                         election_title=election.title,
                         election_id=election.key().id())