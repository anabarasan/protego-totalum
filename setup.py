# setup.py

import webapp2

from app.identity import identity
from app.model import identities, identityHistory
from app.util import renderTemplate

class setupAuthApp(webapp2.RequestHandler):
    def get(self):
        form = """
            <form method='post' action='/setup'>
                administrator@<input type="text" placeholder="domain.com" name="domain" id="domain" style="width:250px;"/><br/>
                <input type="Submit" value="Setup" style="width:250px;"/>
            </form>
        """
        
        cntr = 0
        allidentities = identities.query()
        
        for identity in allidentities:
            cntr += 1
            break
        
        if cntr > 0:
            self.response.out.write(renderTemplate("setup.htm", {'message' : 'Application Setup has already been completed'}))
        else:
            self.response.out.write(renderTemplate("setup.htm", {'message' : form}))
            
    def post(self):
        user = {}
        domain = self.request.get('domain')
        if (domain.strip() == '') or (domain == None):
            domain = "protegototalum.com"
        user['firstName'] = 'Protego Totalum'
        user['lastName'] = 'Administrator'
        user['email'] = 'administrator@%s' % (domain)
        user['password'] = 'password'

        identity('setup').create(user)
        
        self.response.out.write(renderTemplate("setup.htm", {'message' : '<span class = ".title">Application setup has been completed successfully. <br/>Please make a note of the admin user name and password. <br/> UserId : %s <br/> Password : %s</span>' % (user['email'], user['password'])}))
        
app = webapp2.WSGIApplication([('/setup', setupAuthApp)], debug=True)
