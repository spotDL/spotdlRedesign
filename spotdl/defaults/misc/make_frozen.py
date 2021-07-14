"""
The `make_frozen` decorator - ensure that class attributes cannot be modified intensionally or
accidentally except from the classes own member methods.

```python
test_variable = class_decorated_with_make_frozen()

test_variable.set_name(name="NoName")   # Works just fine
test_variable.name = "Name"             # FrozenInstanceError
```
"""

# ===============
# === Imports ===
# ===============
import typing
import inspect


# ===================
# === Make Frozen ===
# ===================


class FrozenInstanceError(Exception):
    """
    ### Overview
    The error that is thrown when an attempt is made to modify an attribute of a class decorated
    with the `make_frozen` decorator

    ### Public Attributes
    - None
    """

    # pylint: disable=too-few-public-methods
    pass


def conditional_setter(self, name: str, value: typing.Any):
    """
    ### Args
    - self: `Any`, refering to current object instance
    - name: `str`, name of the attribute to be set
    - value: `Any`, Value of said attribute

    ### Returns
    - None

    ### Exceptions
    - FrozenInstanceError, this error is thrown when an attempt is made to modify an attribute of
    a class decorated with the `make_frozen` decorator

    ### Function / Notes
    This is an implementation of a conditional `__setattr__` method that only allow setting or
    modifying of class attributes from functions defined within the class itself. It's meant of
    express use with only the `make_frozen` decorator
    """
    # inspect.stack returns a list of named tuples, see:
    # - inspect.stack(): https://docs.python.org/3/library/inspect.html#inspect.stack
    # - FrameInfo https://docs.python.org/3/library/inspect.html#the-interpreter-stack
    caller_name = inspect.stack()[1].function

    class_functions = [
        member[0] for member in inspect.getmembers(self, predicate=inspect.ismethod)
    ]

    # if the caller is one of the class functions, set the required attributes,
    # else, raise FrozenInstanceError
    if caller_name in class_functions:
        object.__setattr__(self, name, value)
    else:
        raise FrozenInstanceError


def make_frozen(cls):
    """
    ### Args
    - cls: `Any`, A class to safeguard from external runtime attribute modifiction/tampering

    ### Returns
    - `Any`, A modified version of the class defined such that a `FrozenInstanceError` is thrown
    when there is an attempt to modify the class from outside of its member functions

    ### Exceptions
    - None
    """

    # Set/Overwrite the default __setattr__ to out custom conditional setter
    setattr(cls, "__setattr__", conditional_setter)

    return cls
