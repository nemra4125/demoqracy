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
from model import Election
try:
  import custom_configuration as configuration
except ImportError:
  import configuration

class PostbackVerifyHandler(BaseHandler):
  def post(self):
    """Handles post request."""
    encoded_jwt = self.request.get('jwt', None)
    if encoded_jwt is not None:
      # jwt.decode won't accept unicode, cast to str
      # http://github.com/progrium/pyjwt/issues/4
      decoded_jwt = jwt.decode(str(encoded_jwt), configuration.SELLER_SECRET)

      # Only update datastore and respond to Google if we have all the values
      # we need. If not, the payment will not go through since the postback
      # will not have a response to validate
      if (decoded_jwt['iss'] == 'Google' and
        decoded_jwt['aud'] == configuration.SELLER_ID):
        if ('response' in decoded_jwt and
            'orderId' in decoded_jwt['response'] and
            'request' in decoded_jwt):
          order_id = decoded_jwt['response']['orderId']
          request_info = decoded_jwt['request']
          if ('currencyCode' in request_info and 'sellerData' in request_info
              and 'name' in request_info and 'price' in request_info):
            election_id = request_info['sellerData']
            election = Election.get_by_id(long(election_id))
            election.ads_enabled = False
            election.put()
