# A Simple Identity app.
# Anbarasan <nasarabna@gmail.com>
# /create     => create a new identity
# /list       => list all identities
# /update     => update an identity
# /delete     => delete an identity
# /identify    => verify if an idenfier is who he is

from datetime import datetime, timedelta
from google.appengine.api import memcache
from app.authentication import customAuthentication as authentication
from app.identity import identity
from app.util import isAuthenticated, renderTemplate
import base64, jinja2, json, logging, webapp2

def handle_error(request, response, exception):
    logging.info("Inside HANDLE_ERROR()")
    logging.exception(exception)
    response.out.write('Oops! I could swear this page was here!')
    response.set_status(405)

class MainHandler(webapp2.RequestHandler):
    def get(self, UserId = None, action = None, Key = None):
        # Check if User Information is available
        if (UserId == None) or (len(UserId) == 0):
            self.response.out.write(renderTemplate("login.htm"))
        else:
            SessionId = self.request.get("session")
            if (isAuthenticated(UserId, SessionId)): # Check if User is logged in and Session is valid
                if ('administrator@' not in UserId) and (action != 'logout'): # Check if User is admin, else redirect to logged in User's Page
                    action = 'update' 
                    Key = str(identity(UserId).getUserById().key.id())
                
                if (action == None) or (len(action.strip()) == 0): # Home Page
                    self.response.out.write(renderTemplate("home.htm", {'userid' : UserId, 'sessionid' : SessionId}))
                else:
                    action = action.strip() # remove leading / trailing spaces
                    if action == 'create':
                        self.response.out.write(renderTemplate('create.htm',{'userid' : UserId, 'sessionid' : SessionId }))
                    elif action == 'list':
                        self.response.out.write(renderTemplate('list.htm',{'userid':UserId, 'sessionid' : SessionId, 'users':identity(UserId).list()}))
                    elif action == 'update':
                        if (len(Key.strip()) == 0):
                            self.error(400) # Bad Request Key not given
                        else:
                            userInstance = identity(UserId, Key.strip())
                            if (UserId == 'admin') or (UserId == userInstance.getUserId()):
                                self.response.out.write(renderTemplate('update.htm',{'userid':UserId, 'sessionid' : SessionId, 'userinfo':identity(UserId, Key.strip()).getUser()}))
                            else:
                                self.response.out.write(renderTemplate('message.htm',{'message' : 'You are not authorized to edit this record', 'redirectURL' : '/%s?session=' % (UserId, SessionId)}))
                    elif action == 'delete':
                        self.error(405) # delete should not be called via GET
                        
                    elif action == 'logout':
                        auth = authentication()
                        auth.logout(SessionId)
                        self.redirect("/")
                    else:
                        self.error(400) # Bad Request. unknown action
            else:
                self.response.out.write(renderTemplate("login.htm"))

    def post(self, UserId, action = None, Key = None):
        SessionId = self.request.get("session")
        if action:
            action = action.strip()
        if action == 'authenticate':
            auth = authentication()
            authenticated, sessionId = auth.authenticate(UserId, self.request.get('Password'))
            if (authenticated):
                self.redirect("/%s?session=%s" % (UserId, sessionId))
            else:
                self.response.out.write(renderTemplate('message.htm',{'message' : 'UserId or Password incorrect.\nPlease try again', 'redirectURL' : '/'}))
        else:
            if (isAuthenticated(UserId, SessionId)): # Check if User is logged in and Session is valid
                if len(action) > 0:
                    if action == 'create':
                        user = {}
                        user['firstName'] = self.request.get('FirstName')
                        user['lastName'] = self.request.get('LastName')
                        user['email'] = self.request.get('EmailAddress')
                        user['password'] = self.request.get('Password')
                        
                        identity(UserId).create(user)
                        
                        self.response.out.write(renderTemplate('message.htm',{'message' : 'User %s %s created successfully' % (user['firstName'], user['lastName']), 'redirectURL' : '/%s?session=%s' % (UserId, SessionId)}))
                        
                    elif action == 'list':
                        self.error(405) # List should not be called via POST
                        
                    elif action == 'update':
                        userInstance = identity(UserId, Key.strip())
                        if (UserId == 'admin') or (UserId == userInstance.getUserId()):
                            user = {}
                            user['firstName'] = self.request.get('FirstName')
                            user['lastName'] = self.request.get('LastName')
                            user['email'] = self.request.get('EmailAddress')
                            user['password'] = self.request.get('Password')
                            
                            userInstance.update(user)
                            
                            self.response.out.write(renderTemplate('message.htm',{'message' : 'User %s %s updated successfully' % (user['firstName'], user['lastName']), 'redirectURL' : '/%s?session=%s' % (UserId, SessionId)}))
                            
                    elif action == 'delete':
                        
                        userInstance = identity(UserId, Key.strip())
                        if (userInstance.getUserId() == UserId):
                            self.response.out.write(renderTemplate('message.htm',{'message' : 'Cannot delete the currently logged in User.\nPlease login as a different user and try again.', 'redirectURL' : '/%s/list?session=%s' % (UserId, SessionId)}))
                        elif (UserId == 'admin') and (userInstance.getUserId() == 'admin'):
                            self.response.out.write(renderTemplate('message.htm',{'message' : 'Only an Admin can delete another admin.', 'redirectURL' : '/%s/list?session=%s' % (UserId, SessionId)}))
                        else:
                            firstName = userInstance.getFirstName()
                            lastName = userInstance.getLastName()
                            
                            userInstance.delete()
                            
                            self.response.out.write(renderTemplate('message.htm',{'message' : 'User %s %s deleted successfully' % (firstName, lastName), 'redirectURL' : '/%s/list?session=%s' % (UserId, SessionId)}))
                            
                    else:
                        self.error(400) # Bad Request. unknown action
                else:
                    self.error(400) # Bad Request. action is not given
            else:
                self.redirect("/")
        
app = webapp2.WSGIApplication([
                        ('/(.*)/(.*)/(.*)', MainHandler),
                        ('/(.*)/(.*)', MainHandler),
                        ('/(.*)', MainHandler)
                        ], debug=True)

app.error_handlers[405] = handle_error
