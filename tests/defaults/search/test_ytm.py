import spotdl.defaults.search.ytm as ytm
import pytest


def test__prepare_word():
    assert (
        ytm.__prepare_word(word="Hello there... General Kenobiahhh!!! *cough* *cough*")
        == "hellotheregeneralkenobiahhhcoughcough"
    )


@pytest.mark.parametrize(
    "src, res, similarity_status",
    [
        ("Käfig", "Kafig", True),
        ("Käfig", "K fig", True),
        ("Käfig", "Kafeg", True),
        ("Käfig", "Kaefg", False),
        ("Käfig", "Kfig", False),
        ("Käfig", "Ka-fig", False),
    ],
)
def test__is_similar(src, res, similarity_status):
    assert ytm.__is_similar(src_word=src, res_word=res) is similarity_status


@pytest.mark.parametrize(
    "src, res, common_fraction",
    [
        ("Hello there general kenobi", "hElLo ThErE GeNeRaL KeNoBi", 1),
        ("Hello there general kenobi", "hElLo ThErE ..//$!@ GeNeRaL KeNoBi", 1),
        ("Hello there general kenobi", "hElLo - ThErE ..//$!@ GeNeRaL KeNoBi", 1),
        ("こんにちは、ケノビ将軍です", "こんにちはケノビ将軍です", 1),
        ("Hello there general kenobi", "hElLo   ThErE ..//$!@ GeNeRaL KeNoBi", 1),
        ("Hello there general kenobi", "hElLo   ThErE GeNeRaL KeNoby", 1),
        ("Hello there general kenobi", "hElLo   ThErE GeNeRaL KeNaby", 1),
        ("Hello there general kenobi", "hElLo   ThErE GeNeRaL KoNaby", 0.75),
    ],
)
def test__common_elm_fraction(src, res, common_fraction):
    assert ytm.__common_elm_fraction(src, res) == common_fraction


@pytest.mark.parametrize(
    "name, artist, check_term",
    [
        ("Linkin Park - Numb (Stylophone cover)", ["maromaro1337"], "Stylophone"),
        ("High School DxD AMV - Courtesy Call", ["Sabishii Tenshi"], "AMV"),
        ("I Don't Care (Switching Vocals)", ["Nightcore Dreams"], "Switching Vocals"),
        ("The Killers 'Mr. Brightside' - Glasgow Festival 2018", ["Luz"], "Festival"),
        ("HAPPY - Pharrell Williams (Female Version)", ["Arlene Zelina"], "Female"),
        ("Adele - Hello (Male Version)", ["MusicEdits"], "Male"),
    ],
)
@pytest.mark.vcr
def test__query_ytmusic_special_cases(name, artist, check_term):
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
def test__query_ytmusic_general_case():
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
