import os
import sys 
import json
import spotipy
import webbrowser
import spotipy.util as util
import json.decoder as JSONDecodeError

# Get the user name from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

#spotify:user:9pc2up6llq5ki85nzcznf2sao

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
#print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
follower = user['followers']['total'] 
print(str(displayName) + " with "+ str(follower)+ " Followers")   