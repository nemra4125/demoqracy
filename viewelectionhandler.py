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

import jwt
import time

from basehandler import BaseHandler
import constants
from model import Election
from webob.exc import HTTPBadRequest
try:
  import custom_configuration as configuration
except ImportError:
  import configuration

class ViewElectionHandler(BaseHandler):
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPBadRequest("That is not a valid election id.")
    election_state = election.GetElectionStateAsJson()
    now = int(time.time())
    now_plus_one = now + 36000
    request_info = {"currencyCode": "USD",
                    "sellerData": election_id,
                    "name": "Go Ads Free",
                    "price": "0.99",
                    "description": "Go ads-free for only $0.99"}
    basic_jwt_info = {"iss": configuration.SELLER_ID,
                      "aud": "Google",
                      "typ": "google/payments/inapp/item/v1",
                      "iat": now,
                      "exp": now_plus_one,
                      "request": request_info}
    item_token = jwt.encode(basic_jwt_info, configuration.SELLER_SECRET)
    election_active = election.CheckStartEndTime()
    countdown_time = 0
    if election_active == constants.NOT_STARTED and election.start:
      countdown_time = int(time.mktime(election.start.timetuple()))
    elif election_active == constants.ACTIVE and election.end:
      countdown_time = int(time.mktime(election.end.timetuple()))
    vote_count, history = election.GetElectionHistory()
    candidates = election.GetCandidateNamesAsJson()
    self.render_template("view.html",
                         election_state=election_state,
                         title=election.title,
                         election_id=election_id,
                         election_active=election_active,
                         countdown_time=countdown_time,
                         total_votes=election.GetElectionHistory()[0],
                         ads_enabled=election.ads_enabled,
                         ads_free_jwt=item_token,
                         vote_count=vote_count - 1,
                         history=history,
                         candidates=candidates,
                         winners=election.GetWinners())