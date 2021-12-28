import pickle
import os.path
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth


def authenticate_spotify():
    scope = "playlist-read-private"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
    return sp


def get_user_playlists(sp):
    playlist_list = []
    playlist_name = []
    results = sp.current_user_playlists(limit=50)

    for i, item in enumerate(results['items']):
        if i > 5:
            break
        playlist_list.append(item['id'])
        playlist_name.append(item['name'])

    return playlist_list, playlist_name


def get_all_songs_from_playlist(user_playlists, sp, playlist_names):
    song_list = []
    for id, name in zip(user_playlists, playlist_names):
        playlist_song_dict = {}
        playlist_items = []
        limit_offset = 0
        while True:
            json_data = sp.playlist_items(playlist_id=id, fields='items.track.id', limit=50, offset=limit_offset)
            limit_offset = limit_offset + 50
            for key in json_data['items']:
                playlist_items.append(key['track']['id'])
            playlist_song_dict[name] = playlist_items
            if len(json_data['items']) < 50:
                break
        song_list.append(playlist_song_dict)
    return song_list


def write_data(song_list):
    songpickle = open('songfile', 'wb')
    pickle.dump(song_list, songpickle)
    songpickle.close()


def read_data(filename):
    pickle_file = open(filename, "rb")
    song_data = pickle.load(pickle_file)
    return song_data


def get_song_features(song_list, sp):
    columns = []
    for playlists in song_list:
        for key, value in playlists.items():
            for index, songs in enumerate(value):
                audio_data = sp.audio_features(songs)
                print(index)
                audio_data[0]["playlist_name"] = key
                if not columns:
                    print(audio_data[0])
                    columns = list(audio_data[0].keys())
                    song_df = pd.DataFrame(columns=columns)
                song_df = song_df.append(audio_data[0], ignore_index=True)
            # print(audio_data[0].keys())
    return song_df



if __name__ == '__main__':
    sp_connection = authenticate_spotify()
    if not os.path.isfile('songfile'):
        playlists, names = get_user_playlists(sp_connection)
        songs = get_all_songs_from_playlist(playlists, sp_connection, names)
        write_data(songs)
    else:
        playlist_tracks = read_data('songfile')

# print(playlist_tracks[0])
df = get_song_features(playlist_tracks, sp_connection)
print(df.head())

    # get_song_features(playlist_tracks)
    # Press Ctrl+F8 to toggle the breakpoint.
    # sp.playlist_items(results['items'][])
    # print(results['items'][0]['id'])
    # field_list = ['items:0:track:name']
    # data = sp.playlist_items(playlist_id=item['id'], limit=1, fields='items.track')
    # print(data['items'][0])