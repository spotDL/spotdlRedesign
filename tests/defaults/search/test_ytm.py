import spotdl.defaults.search.ytm as ytm
import pytest


def test___prepare_word():
    assert (
        ytm.__prepare_word(word="Hello there... General Kenobiahhh!!! *cough* *cough*")
        == "hellotheregeneralkenobiahhhcoughcough"
    )


@pytest.mark.parametrize(
    "src, res, similarity_status",
    [
        ("Käfig", "Kafig", True),  # single-character difference
        ("Käfig", "K fig", True),  # single-character difference (space as character)
        ("Käfig", "Kafeg", True),  # double-character difference
        ("Käfig", "Kaefg", False),  # triple-character difference
        ("Käfig", "Kfig", False),  # shorter word (total-mismatch)
        ("Käfig", "Ka-fig", False),  # longer word (total-mismatch)
    ],
)
def test___is_similar(src, res, similarity_status):
    assert ytm.__is_similar(src_word=src, res_word=res) is similarity_status


@pytest.mark.parametrize(
    "src, res, common_fraction",
    [
        (
            "Hello there general kenobi",
            "hElLo ThErE GeNeRaL KeNoBi",
            1,
        ),  # case-insensitivity
        (
            "Hello there general kenobi",
            "hElLo ThErE Ge..//$!@NeRaL KeNoBi",
            1,
        ),  # ignoring non-alphanumeric characters
        (
            "Hello there general kenobi",
            "hElLo - ThErE ..//$!@ GeNeRaL KeNoBi",
            1,
        ),  # ignoring non-alphanumeric words
        ("こんにちは、ケノビ将軍です", "こんにちはケノビ将軍です", 1),  # non-english results
        (
            "Hello there general kenobi",
            "hElLo   ThErE ..//$!@ GeNeRaL KeNoBi",
            1,
        ),  # multiple consecutive spaces in title
        (
            "Hello there general kenobi",
            "hElLo   ThErE GeNeRaL KeNoby",
            1,
        ),  # ignoring single-character difference is spellings
        (
            "Hello there general kenobi",
            "hElLo   ThErE GeNeRaL KeNaby",
            1,
        ),  # ignoring double-character difference is spellings
        (
            "Hello there general kenobi",
            "hElLo   ThErE GeNeRaL KoNaby",
            0.75,
        ),  # triple-character differences are not ignored
    ],
)
def test___common_elm_fraction(src, res, common_fraction):
    assert ytm.__common_elm_fraction(src, res) == common_fraction


@pytest.mark.parametrize(
    "name, artist, check_term",
    [
        (
            "Linkin Park - Numb (Stylophone cover)",
            ["maromaro1337"],
            "Cover",
        ),  # only "cover" results
        (
            "High School DxD AMV - Courtesy Call",
            ["Sabishii Tenshi"],
            "AMV",
        ),  # only "AMV" results
        (
            "I Don't Care (Switching Vocals)",
            ["Nightcore Dreams"],
            "Switching Vocals",
        ),  # only "switching vocals" results
        (
            "The Killers 'Mr. Brightside' - Glasgow Festival 2018",
            ["Luz"],
            "Festival",
        ),  # only "festival" results
        (
            "HAPPY - Pharrell Williams (Female Version)",
            ["Arlene Zelina"],
            "Female Version",
        ),  # only "female [version]" results
        (
            "Adele - Hello (Male Version)",
            ["MusicEdits"],
            "Male Version",
        ),  # only "male [version]" results
    ],
)
@pytest.mark.vcr
def test___query_ytmusic_special_cases(name, artist, check_term):
    return_results = ytm.__query_ytmusic(
        song_name=name,
        song_artists=artist,
    )

    for result in return_results:
        if check_term.lower() not in result["name"].lower():
            assert False
        else:
            assert True


@pytest.mark.vcr
def test___query_ytmusic_general_case():
    return_results = ytm.__query_ytmusic(
        song_name="Hypnocurrency", song_artists=["Rezz", "deadmau5"]
    )

    for result in return_results:
        for word in [
            "cover",
            "festival",
            "amv",
            "male",
            "female",
            "switching vocals",
        ]:
            if word in result["name"].lower():
                assert False
            else:
                assert True


@pytest.mark.vcr
def test_get_youtube_link():
    return_link = ytm.get_youtube_link(
        song_name="Dancin (Krono Remix)",
        song_artists=["Aaron Smith", "TheSpotdlTeam"],
        song_album="Dancin (Krono Remix)",
        song_duration=1017,
    )

    assert return_link is None
