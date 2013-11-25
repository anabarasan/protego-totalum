# authentication.py
import logging
from datetime import datetime, timedelta
from model import identities, sessions
from google.appengine.ext.ndb import Key

class customAuthentication():
    def authenticate(self, UserId, Password):
        users = identities.query(identities.EmailAddress == UserId)
        
        authuser = {}
        for user in users:
            authuser["firstName"] = user.FirstName
            authuser["lastName"] = user.LastName
            authuser["EmailAddress"] = user.EmailAddress
            authuser["Password"] = user.Password
            break
            
        self.authuser = authuser
        if (authuser["Password"] == Password):
            return True, self.createSession().id()
        else:
            return False, 0
            
    def createSession(self):
        session = sessions()
        session.EmailAddress = self.authuser['EmailAddress']
        session.ExpiresAt = datetime.now()+timedelta(seconds=3600)
        return session.put()
        
    def logout(self, sessionId):
        logging.info("logging out")
        session = Key('sessions',int(sessionId)).get()
        session.ExpiresAt = datetime.now()
        session.put()
