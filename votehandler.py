import datetime
from basehandler import BaseHandler
from google.appengine.api import users
from model import Vote
from google.appengine.ext import db
from webob.exc import HTTPUnauthorized, HTTPBadRequest

class VoteHandler(BaseHandler):
  def get(self, candidate_key):
    voter = users.get_current_user()
    if voter is None:
      raise HTTPUnauthorized("You must be logged in to vote.")
    candidate = db.get(candidate_key)
    if candidate is None:
      raise HTTPBadRequest("Couldn't find candidate with key '%s'." %
                           candidate_key)
    election = candidate.parent()
    vote = Vote(parent=candidate, voter=voter, election=election.key())
    vote.put()