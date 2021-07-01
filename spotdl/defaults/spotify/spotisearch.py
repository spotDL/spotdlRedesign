# pylint: disable=W0511
# pylint: disable=C0301

"""
Tools to search Spotify for a Song match from available data.
"""

# ===============
# === Imports ===
# ===============
from typing import Generator, Any, Optional, AsyncGenerator, List
from itertools import islice
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


def get_playlist(playlist_id: str, number_of_generators: int = 0) -> List[Generator]:
    """
    ### Args
    - playlist_id: `str`, URL/URI/ID of the playlist to be found

    ### Returns
    - `List[Generator]`, list of generators, which each return get_track metadata(s)

    ### Errors raised
    - None

    ### Notes
    - This function only has support for playlists with under 100 tracks (will be increased)
    """
    playlist = sp.playlist_items(playlist_id, limit=100)
    while playlist["next"]:
        next_request = sp.next(playlist)
        playlist["items"].extend(next_request["items"])
        playlist["next"] = next_request["next"]
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
    while album["tracks"]["next"]:
        next_request = sp.next(album["tracks"])
        album["tracks"]["items"].extend(next_request["items"])
        album["tracks"]["next"] = next_request["next"]
    return __generator_loader(album["tracks"], number_of_generators, album=album)


# ========================================================
# === support / helper /background / private functions ===
# ========================================================


def __track_to_metadata(track: dict, album: Optional[dict] = None) -> dict:
    """
    ### Args
    - track: `dict`, Track data to be used to return metadata
    - album: `Optional[Any]`, Album data to replace track album data (needed for get_album)

    ### Returns
    - `dict`, Metadata

    ### Errors raised
    - None

    ### Notes
    - None
    """
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


def __generator_loader(
    item: dict, number_of_generators: int = 5, album: Optional[Any] = False
) -> List[Generator]:
    """
    ### Args
    - item: `dict`, List of tracks to get metadata from
    - number_of_generators: `int`, Number of Generators to create, the number of tracks MUST
    be divisible by the number of tracks or else it will be automatically set to 10
    - album: `Optional[Any]`, Album data to replace track album data (needed for get_album)

    ### Returns
    - `List[Generator]`, list of Generators (__get_playlist_generator)

    ### Errors raised
    - None

    ### Notes
    - None
    """
    items = item["items"]
    if number_of_generators == 0 or len(items) % number_of_generators != 0:
        number_of_generators = 5
    if len(items) < 10:
        number_of_generators = len(items)
    # This changes the number_of_generators to the nearest divisible number
    sections = int(len(items) / number_of_generators)
    return [
        __get_playlist_generator(
            items[previous:section], album=album if album else None
        )
        for section, previous in zip(
            range(sections, len(items) + sections, sections),
            range(0, len(items) + sections, sections),
        )
    ]


async def __convert_to_async(generator: Generator) -> AsyncGenerator:
    """
    ### Args
    - generator: `Generator`, Generator to turn async

    ### Returns
    - `AsyncGenerator`, async Generator

    ### Errors raised
    - None

    ### Notes
    - None
    """
    for each in generator:
        yield each


def __get_playlist_generator(
    list_of_tracks: List[dict], album: Optional[Any] = None, batch_size: int = 10
) -> Generator:
    """
    ### Args
    - list_of_tracks: `List[dict]`, List of tracks to get metadata from
    - album: `Optional[Any]`, Album data to replace track album data (needed for get_album)
    - batch_size: `int`, Batch return size of the generator

    ### Returns
    - `Generator`, Generator, which returns songs in batches of batch_size

    ### Errors raised
    - None

    ### Notes
    - None
    """
    iterations = iter(list_of_tracks)
    for _ in range(0, len(list_of_tracks), batch_size):
        yield [
            __track_to_metadata(
                track["track"] if "track" in track else track,
                album if "track" in track else None,
            )
            for track in islice(iterations, batch_size)
        ]
