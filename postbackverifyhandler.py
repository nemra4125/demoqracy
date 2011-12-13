from basehandler import BaseHandler
from google.appengine.api import users
from google.appengine.ext import db
from model import Candidate, Election
from utils import ProcessParams
from webob.exc import HTTPBadRequest, HTTPUnauthorized
from webapp2_extras.appengine.users import login_required
from sellerinfo import SELLER_ID
from sellerinfo import SELLER_SECRET
import logging

class PostbackVerifyHandler(BaseHandler):

  def post(self):
    """Handles post request."""
    encoded_jwt = self.request.get('jwt', None)
    if encoded_jwt is not None:
      # jwt.decode won't accept unicode, cast to str
      # http://github.com/progrium/pyjwt/issues/4
      decoded_jwt = jwt.decode(str(encoded_jwt), SELLER_SECRET)

      # Only update datastore and respond to Google if we have all the values
      # we need. If not, the payment will not go through since the postback
      # will not have a response to validate
      if decoded_jwt['iss'] == 'Google' and decoded_jwt['aud'] == SELLER_ID:
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
