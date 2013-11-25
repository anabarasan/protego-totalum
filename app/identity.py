# identity.py
# Anbarsan <nasarabna@gmail.com

from datetime import datetime, timedelta
from model import identities, identityHistory
from util import renderTemplate
from google.appengine.ext.ndb import Key
import logging

class identity():
    def __init__(self, currentUser, Id = None):
        self.currentUser = currentUser
        if (Id == None) or (len(Id.strip()) == 0):
            self.identity = identities()
        else:
            self.identity = Key('identities',int(Id)).get()
        self.history = identityHistory()
            
    def create(self, user):
        logging.info("Creating User %s %s with UserId %s" % (user['firstName'], user['lastName'], user['email']))
        
        self.identity.FirstName = user['firstName']
        self.identity.LastName = user['lastName']
        self.identity.EmailAddress = user['email']
        self.identity.Password = user['password']
        
        self.identity.put()
        
        self.updateHistory('Create')
    
    def list(self):
        return self.identity.query()
    
    def update(self, user):
        logging.info("Updating User %s %s with UserId %s" % (self.identity.FirstName, self.identity.LastName, self.identity.EmailAddress))
        
        self.identity.FirstName = user['firstName']
        self.identity.LastName = user['lastName']
        self.identity.EmailAddress = user['email']
        self.identity.Password = user['password']
        
        self.identity.put()
        
        self.updateHistory('Update')
    
    def delete(self):
        logging.info("Deleting User %s %s with UserId %s" % (self.identity.FirstName, self.identity.LastName, self.identity.EmailAddress))
        self.updateHistory('Delete')
        self.identity.key.delete()
        
    def updateHistory(self, action):
        logging.info("updating user history for %s" % (self.identity.FirstName))
        
        self.history.IdentityId = str(self.identity.key.id())
        self.history.FirstName = self.identity.FirstName
        self.history.LastName = self.identity.LastName
        self.history.EmailAddress = self.identity.EmailAddress
        self.history.Password = self.identity.Password
        self.history.Action = action
        self.history.Actor = self.currentUser
        
        self.history.put()
    
    def getUser(self):
        return self.identity
    
    def getUserId(self):
        return self.identity.EmailAddress
        
    def getFirstName(self):
        return self.identity.FirstName
        
    def getLastName(self):
        return self.identity.LastName
        
    def getUserById(self):
        currentuser = ""
        
        userqry = identities.query(identities.EmailAddress == self.currentUser)
        for user in userqry:
            currentuser = user
            break
            
        return currentuser
