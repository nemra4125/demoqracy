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
  def get(self, election_id):
    election = Election.get_by_id(long(election_id))
    if election is None:
      raise HTTPUnauthorized("That is not a valid election id.")
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

    election_active = election.CheckStartEndTime()
    countdown_time = 0
    if election_active == "NOT_STARTED" and election.start:
      countdown_time = int(time.mktime(election.start.timetuple()))
    elif election_active == "ACTIVE" and election.end:
      countdown_time = int(time.mktime(election.end.timetuple()))

    self.render_template("view.html",
                         election_state=election_state,
                         title=election.title,
                         election_id=election_id,
                         election_active=election_active,
                         countdown_time=countdown_time,
                         total_votes=election.GetElectionHistory()[0],
                         ads_enabled=election.ads_enabled,
                         ads_free_jwt=item_token,
                         winners=election.GetWinners())