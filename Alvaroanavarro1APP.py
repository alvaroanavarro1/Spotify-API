import os
import sys 
import json
import spotipy
import webbrowser
import spotipy.util as util
import json.decoder as JSONDecodeError

# Get the user name from terminal
username = sys.argv[1]
scope = 'playlist-modify-public'

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

# User details
displayName = user['display_name']
follower = user['followers']['total']  

while True:

    print("\n Welcome " + str(displayName) + " with "+ str(follower)+ " Followers")  
    print("\n 0 - Search for an artist/band")
    print(" 1 - Exit")
    choice = input("\n Your choice: ")
    choice = int(choice)
    wrongchoice = [2, 3, 4, 5, 6, 7, 8, 9]

    # Prevents wrong choice from the user
    if choice in wrongchoice:
        print("\n Sorry, invalid choice. Try again. \n\n")

    # Search for an Artist/Band
    if choice == 0:
        searchQuery = input("\n Band/Artist name: ")

        # Get search from API
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")
        
        # Artist/Band details
        artist = searchResults['artists']['items'][0]
        print("Band Artist info:")
        print("\n" + str(artist['name']) +  " with " + str(artist['followers']['total']) + " followers")
        print("Genres:")
        print(*artist['genres'], sep=', ')

        webbrowser.open(artist['images'][0]['url'])

        #Album and track details
        albumID = []
        trackURIs = []
        trackArt = []

        # Extract album data 
        artistID = artist['id']
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        # Show Albums from the artist
        for albumNumber,item in enumerate(albumResults):
            print(str(albumNumber) + " - ALBUM "+ item['name'])
            albumID.append(item['id'])
            albumArt = item['images'][0]['url']
        
        playListChoice = input("Deseas crear una lista con las canciones de un album?(Si/No): ")
        
        if playListChoice == "si":
            
            # Create a Playlist with the name of the album
            desiredAlbum = input("Cual album deseas?(Coloque el numero): ")
            desiredAlbum = int(desiredAlbum)
            playListAlbumID = albumID[desiredAlbum]
            playListName = spotifyObject.album(playListAlbumID)
            playListName = playListName['name']
            newPlaylist = spotifyObject.user_playlist_create(username, playListName, public=True, description = "Canciones de album deseado")
            #desiredTracks = spotifyObject.album_tracks()

        if playListChoice == "no":

            noPlayListChoice = input("Quieres buscar otro artista?(Si/No):")

            if noPlayListChoice == "no":
                break
            
            if noPlayListChoice == "si":
                exit

    # Exit Program
    if choice == 1:
        print("\n Until next time")
        break