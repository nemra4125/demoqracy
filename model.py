from datetime import datetime
from google.appengine.ext import db

class Election(db.Model):
  owner = db.UserProperty(required=True)
  title = db.StringProperty(required=True)
  start = db.DateTimeProperty()
  end = db.DateTimeProperty()

  def GetCandidates(self):
    query = Candidate.all().ancestor(self)
    return [candidate for candidate in query]

  def IsActive(self):
    now = datetime.now()
    if self.start is not None and self.start >= now:
      return False
    elif self.end is not None and self.end <= now:
      return False
    return True


class Candidate(db.Model):
  name = db.StringProperty(required=True)

  def GetVoteCount(self):
    query = Vote.all().ancestor(self)
    return query.count()


class Vote(db.Model):
  voter = db.UserProperty(required=True)
  election = db.StringProperty()
  vote_time = db.DateTimeProperty(auto_now_add=True)