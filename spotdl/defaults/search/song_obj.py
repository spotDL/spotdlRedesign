"""
The `Song` class - The sole source of truth about a song's details, you shouldn't have to look
anywhere else for song related details
"""

# ===============
# === Imports ===
# ===============

import typing
from urllib.request import urlopen

from spotdl.defaults.misc.make_frozen import make_frozen


# ====================
# === Actual class ===
# ====================


@make_frozen
class Song:
    """
    ### Overview
    - Acts as the sole source of truth about a song's details

    ### Public attributes
    - source_url: `str`, link to the song on some music streaming platform (usually Spotify)
    - download_url: `str`, link from which to download the best possible match (usually YouTube)
    - song_name: `str`, name of the song
    - album_name: `str`, name of the album to which the song belongs to
    - song_artists: `List[str]`, names of all artits who contributed to the song
    - song_genre: `typing.List[str]`, list of all applicable genres (can be an empty list)
    - song_duration: `int`, length of the song in seconds
    - track_number: `int`, position of track on album disk
    - album_name: `str`, name of the album that the song belongs to
    - album_artists: `typing.List[str]`, names of all artists who contributed to the album the song
    belongs to
    - album_release_year: `int`, the release year of the album (must be a 4 digit number)
    - disk_number: `int`, number of the disk to which the song belongs to (assuming the album has
    multiple disks). You can set this to `1` if no disk number is provided by your source
    - album_art_link: `str`, link from which to download the album art
    - extra_details: `Any`, Extra details related to the song is any format
    - file_name: `str`, a file-system safe file name common to Windows/Linux/MacOS
    """

    # Normally, you should not disable pylint warnings/errors but this is a dataclass and as such
    # it is a necessity as all this call does is validate and store (a lot of) data

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        source_url: str,
        download_url: str,
        song_name: str,
        song_artists: typing.List[str],
        song_genre: typing.List[str],
        song_duration: int,
        track_number: int,
        album_name: str,
        album_artists: typing.List[str],
        album_release_year: int,
        disk_number: int,
        album_art_link: str,
        extra_details: typing.Optional[typing.Any],
    ) -> None:
        """
        ### Args
        - source_url: `str`, link to the song on some music streaming platform (usually Spotify)
        - download_url: `str`, link from which to download the best possible match (usually
        YouTube)
        - song_name: `str`, name of the song
        - album_name: `str`, name of the album to which the song belongs to
        - song_artists: `List[str]`, names of all artits who contributed to the song
        - song_genre: `typing.List[str]`, list of all applicable genres (can be an empty list)
        - song_duration: `int`, length of the song in seconds
        - track_number: `int`, position of track on album disk
        - album_name: `str`, name of the album that the song belongs to
        - album_artists: `typing.List[str]`, names of all artists who contributed to the album the
        song belongs to
        - album_release_year: `int`, the release year of the album (must be a 4 digit number)
        - disk_number: `int`, number of the disk to which the song belongs to (assuming the album
        has multiple disks). You can set this to `1` if no disk number is provided by your source
        - album_art_link: `str`, link from which to download the album art
        - extra_details: `Any | None`, any additional details you would like to save to the `Song`
        object

        ### Returns
        - `Song`, A `Song` object containing the details you just provided

        ### Errors raised
        - `ValueError`, when source_url/download_url or album_art_link are not http/https URLs or
        album_release_year is not a 4 digit number or song_artists/album_artists are empty lists

        ### Notes
        - In case a `ValueError` is thrown, the specific cause is stated in the Traceback, you
        don't have to hunt around
        - To save song details to file, try using `pickle`. It's the easiest way
        """

        # Validate all inputs

        # !check all URLs
        if not source_url.startswith("http"):
            raise ValueError(
                f"source url provided ({source_url}) should be a http/https link"
            )

        if not download_url.startswith("http"):
            raise ValueError(
                f"source url provided ({download_url}) should be a http/https link"
            )

        if not album_art_link.startswith("http"):
            raise ValueError(
                f"source url provided ({album_art_link}) should be a http/https link"
            )

        # !check for empty list inputs
        if len(song_artists) == 0:
            raise ValueError(f"No song artists supplied (song_artists={song_artists}")

        if len(album_artists) == 0:
            raise ValueError(
                f"No album artists supplied (album_artists={album_artists}"
            )

        # !check if album release year is a 4 digit number
        if len(str(album_release_year)) != 4:
            raise ValueError(
                f"album release year provided ({album_release_year}) is not a 4 digit number"
            )

        # Set/Store source/download details
        self.source_url = source_url
        self.download_url = download_url

        # Set/Store song details
        self.song_name = song_name
        self.song_artists = song_artists
        self.song_genre = song_genre
        self.song_duration = song_duration
        self.track_number = track_number

        # Set/Store album details
        self.album_name = album_name
        self.album_artists = album_artists
        self.album_release_year = album_release_year
        self.disk_number = disk_number
        self.album_art = urlopen(album_art_link).read()

        # Set/Store misc details
        self.extra_details = extra_details

        # !Construct a file name that can be used on WIn/Linux/MacOS

        # always include main artist name, this is needed for songs like:
        # Lil Baby, Gunna, Drake - Never Recover (Lil Baby & Gunna, Drake)
        # link at https://open.spotify.com/track/6wWaVoUOzLQJHd3bWAUpdZ
        artist_str = song_artists[0]

        # ! we eliminate contributing artist names that are also in the song name, else we
        # ! would end up with things like 'Jetta, Mastubs - I'd love to change the world
        # ! (Mastubs REMIX).mp3' which is kinda an odd file name.
        for artist in song_artists[1:]:
            if artist.lower() not in song_name.lower():
                artist_str += ", " + artist

        unfinished_file_name = f"{artist_str} - {song_name}"

        # !remove disallowed chars except `"` and `:`
        partial_file_name = "".join(
            character
            for character in unfinished_file_name
            if character not in "/?\\*|<>"
        )

        # !double quotes (") and semi-colons (:) are also disallowed characters but we would
        # !like to retain their equivalents, so they aren't removed in the prior loop
        self.file_name = partial_file_name.replace('"', "'").replace(":", "-")
