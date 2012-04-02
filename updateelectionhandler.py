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
from google.appengine.api import users
from google.appengine.ext import db
from model import Candidate, Election
from utils import ProcessParams
from webob.exc import HTTPBadRequest, HTTPUnauthorized
from webapp2_extras.appengine.users import login_required
import datetime

class UpdateElectionHandler(BaseHandler):

  def post(self, election_id):
    if users.get_current_user() is None:
      raise HTTPUnauthorized("You must be logged in to create a new election.")
    params = ProcessParams(request=self.request,
                           optional_params=["ads_enabled"],
                           required_params=[])

    election = Election.get_by_id(long(election_id))
    if election is None or election.owner != users.get_current_user():
      raise HTTPUnauthorized("You are not the owner of this election.")

    if params["ads_enabled"] == "True":
      election.ads_enabled = True
    else:
      election.ads_enabled = False
    election.put()
    self.render_template("view.html",
                         election_state=election.GetElectionStateAsJson(),
                         title=election.title,
                         election_id=election_id,
                         total_votes=election.GetElectionHistory()[0],
                         ads_enabled=election.ads_enabled)