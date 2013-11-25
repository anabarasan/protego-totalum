# setup.py

import webapp2

from app.identity import identity
from app.model import identities, identityHistory
from app.util import renderTemplate

class setupAuthApp(webapp2.RequestHandler):
    def get(self):
        script = """
        <script>
            var setup = function(){
                form = document.createElement('form');
                form.method='POST';
                form.action = '/setup';
                form.submit();
            }
        </script>
        """
        
        cntr = 0
        allidentities = identities.query()
        
        for identity in allidentities:
            cntr += 1
            break
        
        if cntr > 0:
            self.response.out.write(renderTemplate("setup.htm", {'script' : '', 'message' : 'Application Setup has already been completed'}))
        else:
            self.response.out.write(renderTemplate("setup.htm", {'script' : script, 'message' : '<input type="button" value="Setup" onClick="javascript:setup();" style="width:250px;"/>'}))
            
    def post(self):
        user = {}
        
        user['firstName'] = 'Protego Totalum'
        user['lastName'] = 'Administrator'
        user['email'] = 'administrator@protegototalum.com'
        user['password'] = 'password'

        identity('setup').create(user)
        
        self.response.out.write(renderTemplate("setup.htm", {'script' : '', 'message' : '<span class = ".title">Application setup has been completed successfully. <br/>Please make a note of the admin user name and password. <br/> UserId : %s <br/> Password : %s</span>' % (user['email'], user['password'])}))
        
app = webapp2.WSGIApplication([('/setup', setupAuthApp)], debug=True)
