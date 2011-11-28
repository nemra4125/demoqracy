from google.appengine.ext import db

class Election(db.Model):
  owner = db.UserProperty(required=True)
  title = db.StringProperty(required=True)
  start = db.DateTimeProperty()
  end = db.DateTimeProperty()

  def GetCandidates(self):
    query = Candidate.all()
    query.ancestor(self)
    return [candidate for candidate in query]


class Candidate(db.Model):
  name = db.StringProperty(required=True)

  def GetVoteCount(self):
    query = Vote.all()
    query.ancestor(self)
    return query.count()


class Vote(db.Model):
  voter = db.UserProperty(required=True)
  election = db.StringProperty()
  vote_time = db.DateTimeProperty(auto_now_add=True)