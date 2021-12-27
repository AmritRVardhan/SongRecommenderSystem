import spotipy
from spotipy.oauth2 import SpotifyOAuth


def authenticate_spotify():
    scope = "playlist-read-private"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
    return sp


def get_user_playlists(sp):
    playlist_dict = {}
    playlist_list = []
    results = sp.current_user_playlists(limit=50)

    for i, item in enumerate(results['items']):
        if i > 5:
            break
        playlist_list.append(item['id'])

    return playlist_list

    # Press Ctrl+F8 to toggle the breakpoint.
    # sp.playlist_items(results['items'][])
    # print(results['items'][0]['id'])
    # field_list = ['items:0:track:name']
    # data = sp.playlist_items(playlist_id=item['id'], limit=1, fields='items.track')
    # print(data['items'][0])


def get_all_songs(user_playlists, sp):
    song_list = []
    for id in user_playlists:
        limit_offset = 0
        while True:
            json_data = sp.playlist_items(playlist_id=id, fields='items.track.id', limit=49, offset=limit_offset)
            limit_offset = limit_offset + 50
            for key in json_data['items']:
                song_list.append(key['track']['id'])
            if len(json_data['items']) < 49:
                break
    print(len(song_list))
    # print(json_data)


if __name__ == '__main__':
    sp_connection = authenticate_spotify()
    playlists = get_user_playlists(sp_connection)
    get_all_songs(playlists, sp_connection)

    # print_hi('PyCharmW')
