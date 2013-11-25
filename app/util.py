import jinja2, logging, os
from datetime import datetime, timedelta
from google.appengine.ext.ndb import Key
from model import sessions

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def renderTemplate(template, template_values={}):
    output = jinja_environment.get_template('templates/'+template)
    return output.render(template_values)
    
def isAuthenticated(UserId, SessionId):
    if len(UserId) == 0 or len(SessionId) == 0:
        return False
    else:
        session = Key('sessions',int(SessionId)).get()
        if (session.ExpiresAt > datetime.now() + timedelta(seconds=120)):
            return True
        else:
            return False
