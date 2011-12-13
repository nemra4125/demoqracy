import jwt
import time

from basehandler import BaseHandler
from google.appengine.api import users
from model import Election
from sellerinfo import SELLER_ID
from sellerinfo import SELLER_SECRET
from webapp2_extras.appengine.users import login_required
from webob.exc import HTTPUnauthorized

class ViewElectionHandler(BaseHandler):
  @login_required
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None or election.owner != users.get_current_user():
      raise HTTPUnauthorized("You are not the owner of this election.")
    election_state = election.GetElectionStateAsJson()

    now = int(time.time())
    now_plus_one = now + 36000

    request_info = {'currencyCode': 'USD',
                    'sellerData': election_id,
                    'name': 'Go Ads Free',
                    'price': '0.99',
                    'description': 'Go ads-free for only $0.99'}
    basic_jwt_info = {'iss': SELLER_ID,
                      'aud': 'Google',
                      'typ': 'google/payments/inapp/item/v1',
                      'iat': now,
                      'exp': now_plus_one,
                      'request': request_info}
    item_token = jwt.encode(basic_jwt_info, SELLER_SECRET)

    self.render_template("view.html",
                         election_state=election_state,
                         title=election.title,
                         election_id=election_id,
                         election_is_active=election.IsActive(),
                         total_votes=election.GetElectionHistory()[0],
                         ads_enabled=election.ads_enabled,
                         ads_free_jwt=item_token)

    def post(self, election_id, ads_enabled):
      election = Election.get_by_id(long(election_id))
      if election is None or election.owner != users.get_current_user():
        raise HTTPUnauthorized("You are not the owner of this election.")

      if ads_enabled == "True":
        election.ads_enabled = True
      else:
        election.ads_enabled = False
      election.put()

      now = int(time.time())
      now_plus_one = now + 36000

      request_info = {'currencyCode': 'USD',
                      'sellerData': election_id,
                      'name': 'Go Ads Free',
                      'price': '0.99',
                      'description': 'Go ads-free for only $0.99'}
      basic_jwt_info = {'iss': SELLER_ID,
                        'aud': 'Google',
                        'typ': 'google/payments/inapp/item/v1',
                        'iat': now,
                        'exp': now_plus_one,
                        'request': request_info}
      item_token = jwt.encode(basic_jwt_info, SELLER_SECRET)
      self.render_template("view.html", election_state=election.GetElectionStateAsJson(),
                           title=election.title,
                           election_id=election_id,
                           total_votes=election.GetElectionHistory()[0],
                           ads_enabled=ads_enabled,
                           ads_free_jwt=item_token)