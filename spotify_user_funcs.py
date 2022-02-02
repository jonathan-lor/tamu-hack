import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys

def spotify_token():
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return auth_manager, sp

def select_user(): ## USER INPUT ##
    userID = input("""Enter in the user ID (enter "Exit" to quit): """); print('')
    if ((userID == "exit") or (userID == "Exit") or (userID == "EXIT")):
            sys.exit()
    return userID

def find_playlists(playlists, sp):
    localPlaylists = {}
    playlists_print = "\n"
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            playlists_print += "\t[{}] ".format(i + 1) + playlist['name'] + "\n"
            localPlaylists[playlist['name']] = (playlist['id'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    print(playlists_print.strip("\n"))
    return localPlaylists, playlists_print

def select_playlist(playlists, playlists_print): ## USER INPUT ##
    while (True):
        try:
            selection_str = input("""\nSelect the playlist you wish to see (enter in the number on the left) (enter "Exit" to quit): """); print('')
            selection = int(selection_str)
            if ((selection > len(playlists)) or (selection < 1)):
                raise ValueError
            break
        except:
            if ((selection_str == 'exit') or (selection_str == 'Exit') or (selection_str == 'EXIT')):
                sys.exit()
            print("You must choose from the numbers on the left. Only numeric characters (integers) are accepted.\n")
            print(playlists_print.strip("\n"))
    playlists_list = list(playlists)
    playlist_ID = playlists.get(playlists_list[selection - 1])
    return playlist_ID

def get_playlist_tracks(username, playlist_id, sp, playlists_print, localPlaylists):
    while (True):
        results = sp.user_playlist_tracks(username,playlist_id)
        songs_Data = results['items']

        while results['next']:
            results = sp.next(results)
            songs_Data.extend(results['items'])

        try:
            songs_print = ""

            for i in range(len(songs_Data)):
                validity = songs_Data[i]['track'] ## Sometimes songs are removed and mess with the API calls, leading to tracks with no track names ##
                if (validity == None):
                    song_name = "(empty)"
                else:

                    song_name = validity['name']
                    print("\t[{}]".format(i + 1) , song_name)
                    songs_print += "\t[{}] ".format(i + 1) + song_name + "\n"

            if (len(songs_Data) == 0):
                raise ValueError
            else:
                break
            
        except:
            print("\nOops, something is wrong with that playlist. Try again.\n")
            print(playlists_print.strip("\n"))
            playlist_id = select_playlist(localPlaylists, playlists_print)

    return songs_Data, songs_print

def select_song(songs_Data, songs_print): ## USER INPUT ##
    while (True):
        try:
            selection_str = input("""\nSelect the song you wish to see more about (enter in the number on the left) (enter "Exit" to quit): """); print('')
            selection = int(selection_str)
            if ((selection > len(songs_Data)) or (selection < 1)):
                raise ValueError
            break

        except:
            if ((selection_str == 'exit') or (selection_str == 'Exit') or (selection_str == 'EXIT')):
                sys.exit()
            print("You must choose from the numbers on the left. Only numeric characters (integers) are accepted.\n")
            print(songs_print.strip("\n"))

    singular_song_Data = songs_Data[selection - 1]
    return singular_song_Data

def song_data_print(singular_song_data):
    
    validity = singular_song_data['track'] ## Sometimes songs are removed and mess with the API calls, leading to tracks with no track names or data ##
    if (validity == None):
        print("\tThis song was removed from the playlist at somepoint...\n\tThere is nothing to display here")
        return
    
    else:
        song_str = ""
        song_str += "\t[Title:] {}\n".format(singular_song_data['track']['name'])
        song_str += "\t[Album:] {}\n".format(singular_song_data['track']['album']['name'])
        song_str += "\t[Artist:] {}\n".format(singular_song_data['track']['artists'][0]['name'])
        if singular_song_data['track']['explicit']:
            song_str += "\t[Explicit?:] Yes\n"
        else:
            song_str += "\t[Explicit?:] No\n"
        song_str += "\t[Date added:] {}".format(singular_song_data['added_at'])
        print(song_str)

    return

def select_stay(): ## USER INPUT ##
    while (True):
        try:
            selection = input("""\nEnter if you wish to remain on this user's library or move on to a different user's library ("Yes" to remain. "No" to switch) (enter "Exit" to quit): """); print("")
            
            if ((selection == "Y") or (selection == "y") or (selection == "Yes") or (selection == "yes")):
                selection = True
            elif ((selection == "N") or (selection == "n") or (selection == "No") or (selection == "no")):
                selection = False
            else:
                raise ValueError
            break

        except:
            if ((selection == "exit") or (selection == "Exit") or (selection == "EXIT")):
                sys.exit()
            print("You must choose from the options given. Only yes or no (or exit).")

    return selection