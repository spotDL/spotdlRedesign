"""
Tools to search YouTube Music for a Song match from available metadata.
"""

# ===============
# === Imports ===
# ===============
import typing

from ytmusicapi import YTMusic


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
        - name: `str`, name of the result
        - album: `Optional[str]`, name of the result's album if available, else `None`
        - duration: `int`, length of the result in seconds
        - artists: `List[str]`, names of all contributing artists or usename of uploader
        - link: `str`, youtube link

    ### Errors raised
    - None

    ### Function / Notes
    - We assume that results are always found
    - Results with the words "cover", "festival", "amv", "male", "female" or "switching vocals"
    are dumped. The words "male" and "female" are included to handle "Male Version" &
    "Female Version" type song covers.
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
        res_artists = []
        for artist in result["artists"]:
            res_artists.append(artist["name"])

        # !validate the results title
        # 'male' and 'female' are included for 'male version'/'female version' results to be
        # filtered out
        skip_result = False

        for word in [
            "cover",
            "festival",
            "amv",
            "male",
            "female",
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

        res_name = result["title"]

        simplified_results.append(
            {
                "name": res_name,
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
