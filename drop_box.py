# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 23:52:53 2017

@author: Josh Boone
"""

import os.path
import dropbox
from dropbox import oauth
import webbrowser

def main():
    #get the DropBox authorization token from file, if it exists
    auth_token = ""
    if os.path.exists("user_auth.dat"):
        with open("user_auth.dat") as auth_file:
            auth_token = auth_file.read()
    else: #no DropBox token - user must authorize application
        #get the app key and secret from file
        try:
            with open("my_pi_photo_frame_db.dat") as data_file:
                lines = data_file.read().splitlines()
                app_key = lines[0]
                app_secret = lines[1]
        except OSError:
            print "The my_pi_photo_frame_db.dat file is missing or corrupted. Please reinstall the application."
            raise SystemExit
        #start the OAuth2 app authoriztion process
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        #get the authorization URL from the API
        auth_url = auth_flow.start()
        print "Authorize My Pi Photo Frame in the browser window. Copy the authorization code and paste it below."
        #open a web browser to allow the user to authorize the app with DropBox
        webbrowser.open(auth_url)
        auth_code = raw_input("Enter the authorization code here: ").strip()
        try:
            auth_result = auth_flow.finish(auth_code)
            auth_token = auth_result.access_token
        except oauth.BadRequestException, e:
            print "The URL " + auth_url + " was not correct. Error: %s" % (e,)
            raise SystemExit
        except oauth.BadStateException, e:
            #bad state, restart the authorization process
            print "The application encountered a bad state exception. Restarting the authorization process..."
            main()
        except oauth.CsrfException, e:
            print "State query parameter does not contain CSRF token from user session!"
            raise SystemExit
        #write the authorization code to file for future use
        with open('user_auth.dat', 'w') as auth_file:
            auth_file.write(auth_token)
    
if __name__ == "__main__":
    main()        