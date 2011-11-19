from google.appengine.ext import db

class Election(db.Model):
  owner = db.UserProperty(required=True)
  title = db.StringProperty(required=True)
  start = db.DateTimeProperty()
  end = db.DateTimeProperty()


class Candidate(db.Model):
  name = db.StringProperty(required=True)


class Vote(db.Model):
  voter = db.UserProperty(required=True)
  election = db.StringProperty()
  vote_time = db.DateTimeProperty(auto_now_add=True)