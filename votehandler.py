import datetime
from basehandler import BaseHandler
from google.appengine.api import users
from model import Vote
from google.appengine.ext import db

class VoteHandler(BaseHandler):
  def post(self, candidate_key):
    voter = users.get_current_user()
    if voter is None:
      raise UserWarning("You must be logged in to vote.")
    candidate = db.get(candidate_key)
    election = candidate.parent()
    vote = Vote(parent=candidate, voter=voter)
    vote.put()