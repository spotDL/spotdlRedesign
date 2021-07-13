# ===============
# === Imports ===
# ===============
import typing
import pytest
import spotdl.defaults.misc.make_frozen as make_frozen


# ==================
# === Test class ===
# ==================


@make_frozen.make_frozen
class DummyClass:
    def create_attr(self, data: typing.Any) -> None:
        self.data = data

    def modify_attr(self, new_data: typing.Any) -> None:
        self.data = new_data


# ===================
# === Actual test ===
# ===================
def test_make_frozen():
    dummy_instance = DummyClass()

    try:
        dummy_instance.create_attr("random string")
        assert dummy_instance.data == "random string"

        dummy_instance.modify_attr("another random string")
        assert dummy_instance.data == "another random string"

    except:
        assert False

    with pytest.raises(make_frozen.FrozenInstanceError):
        dummy_instance.data = "this setattr call should raise an error"
