# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from basehandler import BaseHandler
from google.appengine.api import taskqueue, users
from google.appengine.ext import db
from model import Candidate, Election
from utils import ProcessParams
from webob.exc import HTTPBadRequest, HTTPUnauthorized
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
    if (not isinstance(params["candidates"], list)
      or len(params["candidates"]) < 2):
      raise HTTPBadRequest("At least two candidates are required.")
    # NOTE: Cross-group transcations requires using the high-replication
    # datastore. Add the --high_replication command line flag to
    # dev_appserver.py in the development environment.
    db.run_in_transaction_options(db.create_transaction_options(xg=True),
                                  self.CreateElectionAndCandidates, params)

  def CreateElectionAndCandidates(self, params):
    record_voter_email = False
    election = Election(title=params["title"], owner=users.get_current_user())
    if "start_ts" in params:
      try:
        election.start = datetime.datetime.fromtimestamp(
          float(params["start_ts"]))
      except ValueError:
        pass
    if "end_ts" in params:
      try:
        election.end = datetime.datetime.fromtimestamp(float(params["end_ts"]))
      except ValueError:
        pass
    election.put()
    for name in params["candidates"]:
      if name:
        candidate = Candidate(parent=election, name=name)
        candidate.put()
    self.render_template("create.html",
                         render_form=False,
                         election_title=election.title,
                         election_id=election.key().id())
    if election.end:
      try:
        taskqueue.add(url="/elections/%d/notify_owner" % election.key().id(),
                      eta=election.end)
      except taskqueue.InvalidTaskError:
        # This is thrown when the task is more than 30 days in the future.
        # Not much we can do here--email notifications won't be sent.
        pass