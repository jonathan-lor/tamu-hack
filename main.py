from spotipy.oauth2 import SpotifyClientCredentials
import os

from spotify_user_funcs import select_song, spotify_token, select_user, find_playlists, select_playlist, get_playlist_tracks, select_song, song_data_print, select_stay

os.environ['SPOTIPY_CLIENT_ID'] = '1b029d0954a14aacb12e726007504621'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'd715fb2684c146b88c13a58f02820c15'
auth_manager, sp = spotify_token()

check = False
print('') ## Add some breathing room ##
while (True):
    if (check == False):
        userID = select_user() ## Enter the USERNAME (not display name) ##

    playlists = sp.user_playlists(userID) ## Creates a LARGE dictionary with all of the user's data from their playlists ##

    localPlaylists, playlists_print = find_playlists(playlists, sp) ## Creates a playlist list, saves it as a dictionary to select from, and prints it ##

    playlist_ID = select_playlist(localPlaylists, playlists_print) ## Allows you to select which playlist you want to see the songs of ##

    songs_Data, songs_print = get_playlist_tracks(userID, playlist_ID, sp, playlists_print, localPlaylists) ## Prints out the songs in the playlist ##

    singular_song_Data = select_song(songs_Data, songs_print) ## Extracts the data for the chosen song ##

    song_data_print(singular_song_Data) ## Prints the data for the song ##

    check = select_stay() ## Can choose whether to stay on the current user, change the user, or exit altogether ##
