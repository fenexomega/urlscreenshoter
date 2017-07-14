from imgurpython import ImgurClient 
from datetime import datetime
from configparser import ConfigParser
import os

CONFIG_FILE = os.path.join(os.environ['HOME'],'.url_screenshoter')

class ImgurHelper:
    client = None

    def __init__(self, client_id,client_secret):
        self.authenticate(client_id, client_secret)

    def parseconfig(self,file):
        if not os.path.isfile(file):
            return False
        
        section = 'config'
        dict  = {}
        config = ConfigParser()
        config.read(file)
        for c in ['access_token','refresh_token']:
            dict[c] = config.get(section,c)
        return dict
    
    def writeconfig(self,file,values):
        f = open(file,'w')
        config = ConfigParser()
        section = 'config'
        config.add_section(section)
        for k,v in values.items():
            config.set(section,k,str(v))
        config.write(f)


    def authenticate(self, client_id, client_secret):
        self.client = ImgurClient(client_id, client_secret)

        credentials = self.parseconfig(CONFIG_FILE)
        # Authorization flow, pin example (see docs for other auth types)
        if credentials == False:
            authorization_url = self.client.get_auth_url('pin')
            
            print("I need access from your Imgur account.")
            print("Go to the following URL: {0}".format(authorization_url))
            # Read in the pin, handle Python 2 or 3 here
            pin = input("Enter pin code: ")

            # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
            credentials = self.client.authorize(pin, 'pin')
            self.writeconfig(CONFIG_FILE,credentials)

            print("Your authentication is saved. You will need to authenticate it again 1 month from now.")

        self.client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

        print("Authentication successful!")

    def upload(self,image_dir):

        # Here's the metadata for the upload. All of these are optional, including
        # this config dict itself.
        date = datetime.now()
        config = {
            'album': None,
            'name':  date,
            'title': date,
            'description': 'Tirado em {}.'.format(datetime.now())
        }   

        image = self.client.upload_from_path(image_dir, config=config, anon=False)
        return image

