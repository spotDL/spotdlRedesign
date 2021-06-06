# This is is kinda hacky but the tests won't run without this. Not sure why.

try:
    import spotdl
except:
    import sys, os

    sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
