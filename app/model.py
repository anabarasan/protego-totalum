# Model.py
# Anbarasan <nasarabna@gmail.com>

from google.appengine.ext import ndb

# Model to store Identity Information
class identities(ndb.Model):
    FirstName       = ndb.StringProperty()
    LastName        = ndb.StringProperty()
    EmailAddress    = ndb.StringProperty()
    Password        = ndb.StringProperty()
    
# Model to store History Information
class identityHistory(ndb.Model):
    IdentityId      = ndb.StringProperty()
    FirstName       = ndb.StringProperty()
    LastName        = ndb.StringProperty()
    EmailAddress    = ndb.StringProperty()
    Password        = ndb.StringProperty()
    Action          = ndb.StringProperty()
    Actor           = ndb.StringProperty()
    TimeStamp       = ndb.DateTimeProperty(auto_now_add=True)
    
# Model to store Session Information
class sessions(ndb.Model):
    EmailAddress    = ndb.StringProperty()
    LoggedInAt      = ndb.DateTimeProperty(auto_now_add=True)
    ExpiresAt       = ndb.DateTimeProperty()
