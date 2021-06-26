# pylint: disable=W0511

"""
Tools to search Spotify for a Song match from available data.
"""

# ===============
# === Imports ===
# ===============
from typing import Generator
from spotipy.oauth2 import SpotifyClientCredentials

import spotipy

CLIENT_ID = "b7f76c8bc8a24622943cb669bde63bb4"
CLIENT_SECRET = "c391f5ff3f87401a96dfecb462b0684e"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))


def get_track(song_name: str) -> dict:
    """
    ### Args
    - song_name: `str`, name of the song to be found

    ### Returns
    - `dict`, metadata of the song found from song_name

    ### Errors raised
    - None

    ### Notes
    - This function may not return the correct song all the time because spotify automatically
    filters search results by popularity, meaning uncommon songs are more likely not to be found
    """
    result = sp.search(q=song_name, limit=5, type="track")
    # This code fixes some song searches
    track = None
    for search in result["tracks"]["items"]:
        if song_name.lower() in search["name"].lower():
            track = search
            break
    if track is None:
        track = result["tracks"]["items"][0]
    return __track_to_metadata(track)


def get_playlist(playlist_id: str, number_of_generators: int = 0) -> list:
    """
    ### Args
    - playlist_id: `str`, URL/URI/ID of the playlist to be found

    ### Returns
    - `list`, list of generators, which each return get_track metadata(s)

    ### Errors raised
    - None

    ### Notes
    - This function only has support for playlists with under 100 tracks (will be increased)
    """
    playlist = sp.playlist_items(playlist_id, limit=100)
    offset = 0
    while playlist['next'] is not None:
        offset += 100
        next_request = sp.playlist_items(playlist_id, limit=100, offset=offset)
        playlist['items'] += next_request['items']
        playlist['next'] = next_request['next']
    return __generator_loader(playlist, number_of_generators)


def get_album(album_id: str, number_of_generators: int = 0) -> list:
    """
    ### Args
    - album_id: `str`, URL/URI/ID of the album to be found

    ### Returns
    - `list`, list of generators, which each return get_track metadata(s)

    ### Errors raised
    - None

    ### Notes
    - This function only has support for albums with under 50 tracks (will be increased)
    """
    album = sp.album(album_id)
    offset = 0
    while album['tracks']['next'] is not None:
        offset += 50
        next_request = sp.album_tracks(album_id, offset=offset)
        album['tracks']['items'] += next_request['items']
        album['tracks']['next'] = next_request['next']
    return __generator_loader(album["tracks"], number_of_generators, isalbum=album)


# ========================================================
# === support / helper /background / private functions ===
# ========================================================


def __track_to_metadata(track, album=None):
    if album is None:
        album = sp.album(track["album"]["external_urls"]["spotify"])
    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    return {
        "URL": track["external_urls"]["spotify"],
        "name": track["name"],
        "artists": [artist["name"] for artist in track["artists"]],
        "genres": (album["genres"] + artist["genres"]),
        "duration": track["duration_ms"],  # milliseconds
        "dt_numbers": [track["disc_number"], track["track_number"]],
        "album_art": album["images"][0],
        "album_name": album["name"],
        "album_artists": [artist["name"] for artist in album["artists"]],
        "album_release": album["release_date"],  # str
    }


def __generator_loader(item, number_of_generators: int = 0, isalbum=False):
    # if number_of_generators is 0 or is invalid (eg. number_of_generators is 5 but amount of tracks
    # is 23 (would be uneven and hard to handle, however this could probably be added with a plugin)
    items = item["items"]
    if number_of_generators == 0 or len(items) % number_of_generators == 0:
        number_of_generators = 10
    if len(items) < 10:
        number_of_generators = len(items)
    sections = int(len(items) / number_of_generators)

    previous = 0
    generators = []
    for section in range(sections, len(items) + sections, sections):
        if isalbum:
            generators.append(
                __get_playlist_generator(items[previous:section], album=isalbum)
            )
        else:
            generators.append(__get_playlist_generator(items[previous:section]))
        previous += sections
    return generators


async def __convert_to_async(generator: Generator):
    """
    ### Args
    - generator: `Generator`, Generator to turn async

    ### Returns
    - `Generator`, async Generator

    ### Errors raised
    - None

    ### Notes
    - None
    """
    for each in generator:
        yield each


def __get_playlist_generator(list_of_tracks: list, batch_size: int = 10, album=None):
    left = len(list_of_tracks)
    while left > 0:
        iterations = left
        if left > batch_size:
            iterations = batch_size
        for track in list_of_tracks:
            if "track" in track:
                yield [__track_to_metadata(track["track"]) for track in list_of_tracks]
            else:
                yield [__track_to_metadata(track, album) for track in list_of_tracks]
        left -= iterations
