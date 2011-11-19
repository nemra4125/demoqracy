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
    query = Vote.all()
    query.filter("voter =", voter)
    query.filter("election =", str(election.key()))
    if query.get() is None:
      vote = Vote(parent=candidate, voter=voter, election=str(election.key()))
      vote.put()
    else:
      raise HTTPBadRequest("You've already voted in this election.")