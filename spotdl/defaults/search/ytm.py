"""
Tools to search YouTube Music for a Song match from available metadata.
"""

# ===============
# === Imports ===
# ===============
import typing

from ytmusicapi import YTMusic


# =============================
# === main / defaults-layer ===
# =============================
def get_youtube_link(
    song_name: str, song_artists: typing.List[str], song_album: str, song_duration: int
) -> typing.Optional[str]:
    """
    ### Args
    - song_name: `str`, name of the song to be found
    - song_artists: `List[str]`, list of contributing artits to the said song
    - song_album: `str`, name of the album to which said song belongs to
    - song_duration: `int`, length of the song in seconds

    ### Returns
    - `str` if a reasonable match is found, the (supposed) best video on YouTube for the said song
    - `None` if all results found are likely to be wrong

    ### Errors raised
    - None

    ### Function / Notes
    - duration_match =  \\(1 - \\frac{\\Delta time}{15}\\). If the time difference between source
    data and YTM result is greater than 15 seconds, we assume the result is incorrect. The
    \\(\\frac{\\Delta time}{15}\\) is the actual match measure, smaller the better. the
    "1-" part (a) flips this to greater is better to keep inline with the other measures and
    (b) makes duration_match negative if \\(\\Delta time > 15\\), such results with negative match
    values are dumped.

    - album_match is either 0 or 1, no intermediate values. Song results with a perfect
    album match are assigned 1, video results are assigned 0, Song results with an incorrect
    album match are dumped, the idea is that if the album is different, even if the result is
    very close by other metrics, it's definitely not the same Song.

    - name_match = \\(\\frac{\\text{number of common words between song name and result title}}
    {\\text{number of words in the bigger one}}\\), if the value of name_match is less than 0.1,
    the result is dropped. It's common sense, more extra words in the name, farther from the
    actual song it is. The cut-off value of 0.1 was reached after running a sample search of
    100 Songs.

    - artist_match = \\(\\frac{\\text{number of common artists between song and result}}
    {\\text{number of artists in the bigger one}}\\), the cut-off here is 0. This is because,
    YouTube Music supplies the username of the uploader if Song Artists aren't known - there might
    be cases with no common artists.

    - avg_match = average of all the above, this is the deciding factor. The link to the result with
    the highest average match is what is actually returned.

    - The number of common words is slightly fuzzy, *'Vogel Im Kafig'* will be matched against
    *'Vogel Im Käfig'* with a score 3-on-3 in spite of the fact that *'kafig'* is not the exact
    same as *'Käfig'*
    """
    ytm_results = __query_ytmusic(song_name=song_name, song_artists=song_artists)

    top_match_score = 0
    top_result = None

    for result in ytm_results:
        # !name_match
        name_match = __common_elm_fraction(src=song_name, res=result["name"])
        if name_match < 0.1:
            continue

        # !album_match
        if result["album"] is None:
            album_match = 0
        else:
            if result["album"].lower() == song_album.lower():
                album_match = 1
            else:
                # song from a different album, definitely not what we want, skip it
                continue

        # !duration match
        delta = abs(result["duration"] - song_duration)
        duration_match = 1 - (delta / 15)

        if duration_match < 0:
            continue

        # !artist_match
        artist_match = __common_elm_fraction(src=song_artists, res=result["artists"])

        # !avg_match and top_result update
        avg_match = (name_match + album_match + duration_match + artist_match) / 4

        if avg_match > top_match_score:
            top_match_score = avg_match
            top_result = result

    if top_match_score <= 0.75:
        if top_result is not None:
            with open("possible errors.txt", "ab") as file:

                file.write(
                    f"{', '.join(song_artists)} - {song_name}\n {top_match_score:0.2f}pt "
                    f"{top_result['link']}: {top_result['name']}\n".encode()
                )
        else:
            with open("skipped.txt", "ab") as file:
                file.write(f"{', '.join(song_artists)} - {song_name}\n".encode())

    if top_result is None:
        return None

    return top_result["link"]


# ========================================================
# === support / helper /background / private functions ===
# ========================================================
def __query_ytmusic(
    song_name: str, song_artists: typing.List[str]
) -> typing.List[dict]:
    """
    ### Args
    - song_name: `str`, name of the song to be found
    - song_artists: `List[str]`, list of all contributing artists

    ### Returns
    - `List[dict]`, [YTM](https://music.youtube.com) query results as dict. Each dict contains the
    following keys:
        - name: `str`, name/title of the result
        - album: `Optional[str]`, name of the result's album if available, else `None`
        - duration: `int`, length of the result in seconds
        - artists: `List[str]`, names of all contributing artists or usename of uploader
        - link: `str`, youtube link

    ### Errors raised
    - None

    ### Function / Notes
    - We assume that results are always found
    - Results with the words "cover", "festival", "amv", "male version", "female version" or
    "switching vocals" are dumped.
    """

    # !construct query and get results
    query = f"{', '.join(song_artists)} - {song_name}"

    ytm_client = YTMusic()
    search_results = ytm_client.search(query=query, filter="videos")
    search_results += ytm_client.search(query=query, filter="songs")

    simplified_results = []

    for result in search_results:
        # !validate 'album' field & determine the return dict's 'album' field
        if result["resultType"] == "song":
            if result["album"] is None:
                continue

            res_album = result["album"]["name"]
        else:
            res_album = None

        # !validate & parse duration for the return dict's 'duration' field
        try:
            # hh:mm:ss --> [ss, mm, hh]
            time_bits = list(reversed(result["duration"].split(":")))

            # for None / other non string return types
            if not isinstance(result["duration"], str) or len(time_bits) > 3:
                continue

            res_duration = sum(a * int(b) for a, b in zip([1, 60, 3600], time_bits))
        except ValueError:
            # These errors get throws when the duration returned is not in the form hh:mm:ss
            # Sometimes, the duration itself is not returned - we can't evaluate such results
            # such results are dropped
            continue

        # !determine the return dict's 'artists' field
        # we assume that the result's 'artists' field is never `None` as YTM returns the uploader's
        # username if the song's artist is unknown (which is usually what happens for videos)
        res_artists = [artist["name"] for artist in result["artists"]]

        # !validate the results title
        # 'male' and 'female' are included for 'male version'/'female version' results to be
        # filtered out
        skip_result = False

        for word in [
            "cover",
            "festival",
            "amv",
            "male version",
            "female version",
            "switching vocals",
        ]:
            # !word in title but not in song_name -> its an unnecessary result
            #
            # !word in song name but not in title -> its not a "cover" or specific version like
            # !we're searching for
            if (word in result["title"].lower() and word not in song_name.lower()) or (
                word in song_name.lower() and word not in result["title"].lower()
            ):
                skip_result = True
                break

        if skip_result:
            continue

        simplified_results.append(
            {
                "name": result["title"],
                "artists": res_artists,
                "album": res_album,
                "duration": res_duration,
                "link": f"https://www.youtube.com/watch?v={result['videoId']}",
            }
        )

    return simplified_results


def __common_elm_fraction(
    src: typing.Union[typing.List[str], str],
    res: typing.Union[typing.List[str], str],
) -> float:
    """
    ### Args
    - src_list: `Union[List[str], str]`, a sentence of set of words to be compared
    - res_list: `Union[List[str], str]`, a sentence of set of words to be compared against

    ### Returns
    - `float`, \\(\\frac{\\text{number of common words between the two strings/lists}}
    {\\text{number of words in the bigger string/list}}\\)

    ### Errors raised
    - None
    """
    # !construct set's of prepared words
    if isinstance(src, str):
        src = src.split(" ")

    if isinstance(res, str):
        res = res.split(" ")

    src_set = set(__prepare_word(word=word) for word in set(src))
    res_set = set(__prepare_word(word=word) for word in set(res))

    if "" in src_set:
        src_set.remove("")

    if "" in res_set:
        res_set.remove("")

    # !find number of common words
    common_words = 0
    for src_word in src_set:
        for res_word in res_set:
            if __is_similar(src_word=src_word, res_word=res_word):
                common_words += 1

                # go to next word from outer set, (probably) nothing else is going to match,
                # even if it did it's likely to be a erroneous
                break

    # !which is greater?
    if len(src_set) > len(res_set):
        greater_word_length = len(src_set)
    else:
        greater_word_length = len(res_set)

    return common_words / greater_word_length


def __prepare_word(word: str) -> str:
    """
    ### Args
    - word: `str`, word to be processed

    ### Returns
    - `str`, word with all non-alphanumeric characters removed in lower case (spaces
    are removed too)

    ### Errors raised
    - None
    """
    prepared_word = ""

    for letter in word:
        if letter.isalnum():
            prepared_word += letter

    return prepared_word.lower()


def __is_similar(src_word: str, res_word: str) -> bool:
    """
    ### Args
    - src_word: `str`, word to be compared
    - res_word: `str`, word to be compared against

    ### Returns
    - `bool`, True if words are similar, else false

    ### Errors raised
    - None

    ### Functioning / Notes
    - Let's say you were comparing 2 song names: *'Vogel Im Kafig'* against *'Vogel Im Käfig'*
    on a word to word basis, direct equality of strings would mean *'Kafig'* is not the same
    as *'Käfig'*. Similarly, you would face the same issue with misspelt titles. This function
    handles that by allowing at max 2 single character mismatches (a -> ä would be a single
    mismatch) before deciding that 2 words are dissimilar.
    """
    # You might notice the lack of the 'else' part of the traditional if-else statements,
    # that is because pylint has an issue with it. See: https://stackoverflow.com/q/63755912
    if src_word == res_word:
        return True

    if not len(src_word) == len(res_word):
        return False

    difference_count = 0

    for _i in range(len(src_word)):
        if src_word[_i] != res_word[_i]:
            difference_count += 1

    if difference_count > 2:
        return False

    return True
