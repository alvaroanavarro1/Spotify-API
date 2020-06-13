from app import app
from flask import render_template, request
import os
import sys 
import json
import spotipy
import spotipy.util as util
import json.decoder as JSONDecodeError
import numpy as np 
import pandas as pd

@app.route('/')
def index():
    # Get the user name from terminal
    global username
    username = sys.argv[0]
    scope = 'playlist-modify-public'

    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username, scope)
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope)

    print(username)
    # Create our spotifyObject
    global spotifyObject
    spotifyObject = spotipy.Spotify(auth=token)

    user = spotifyObject.current_user()
    # User details
    global displayName
    global follower

    displayName = user['display_name']
    follower = user['followers']['total']

    return render_template('public/index.html', displayName = displayName, follower = follower)


@app.route('/band', methods=['GET', 'POST'])
def band():
    if request.method == 'POST':
        searchQuery = request.form['searchQuery']

         # Get search from API
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")

        # Artist/Band details
        artist = searchResults['artists']['items'][0]
        artistName = searchQuery
        artistFollowers = artist['followers']['total']
        artistGenres = artist['genres']
        artistGenres = ', '.join(artistGenres)
        artistImg = artist['images'][0]['url']

        #Album details
        global albumName
        global albumID
        albumName = []
        albumID = []

        # Extract album data 
        artistID = artist['id']
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        # Show Albums from the artist
        for item in albumResults:
            albumName.append(item['name'])
            albumID.append(item['id'])
        
        albumName = ', '.join(albumName)
        

        return render_template('public/band.html', artistName = artistName, artistFollowers = artistFollowers,
                                artistGenres = artistGenres, artistImg = artistImg, albumName = albumName )
        


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    if request.method == 'POST':
        playListChoice = request.form['playListChoice']

        position = albumName.index(playListChoice)
        playListAlbumID = albumID[position]
        playListData = spotifyObject.album(playListAlbumID)
        playListName = playListData['name']
        playListArt = playListData['images'][0]['url']
        #newPlaylist = spotifyObject.user_playlist_create(username, playListName, public=True, description = "Canciones de album deseado")
        #newPlaylistId = newPlaylist['id']

        # Extract track data
        desiredTracks = spotifyObject.album_tracks(playListAlbumID)
        desiredTracks = desiredTracks['items']
        trackURIs = []
        trackNames = []

        for item in desiredTracks:
            trackNames.append(item['name'])
            trackURIs.append(item['uri'])

        trackNames = ', '.join(trackNames)
        
        
        #Create the playlist 
        #spotifyObject.user_playlist_add_tracks(username, newPlaylistId, trackURIs, position=None)
        
        return render_template('public/playlist.html', playListName = playListName, playListArt = playListArt, trackNames = trackNames)

        


