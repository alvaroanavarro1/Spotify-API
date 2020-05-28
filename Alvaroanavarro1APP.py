import os
import sys 
import json
import spotipy
import webbrowser
import spotipy.util as util
import json.decoder as JSONDecodeError

# Get the user name from terminal
username = sys.argv[1]
#scope = 'user-read-private user-read-playback-state user-modify-playback-state'

#spotify:user:9pc2up6llq5ki85nzcznf2sao

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# Create our spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
#print(json.dumps(user, sort_keys=True, indent=4))

# User details
displayName = user['display_name']
follower = user['followers']['total']  

while True:

    print("\n Welcome " + str(displayName) + " with "+ str(follower)+ " Followers")  
    print("\n 0 - Search for an artist/band")
    print(" 1 - Exit")
    choice = input("\n Your choice: ")
    choice = int(choice)

    # Search for an Artist/Band
    if choice == 0:
        searchQuery = input("\n Band/Artist name: ")

        # Get search from API
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")
        
        # Artist/Band details
        artist = searchResults['artists']['items'][0]
        print(str(artist['name']) + " " + str(artist['genres']))

        #webbrowser.open(artist['images'][0]['url'])

        #Album and track details

        

    # Exit Program
    if choice == 1:
        print("\n Until next time")
        break

    else:
        print("\n Sorry, invalid choice. Try again.")
        