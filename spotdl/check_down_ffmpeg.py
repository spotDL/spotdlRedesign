# pylint: disable=line-too-long
# pylint: disable=consider-using-with
# pylint: disable=superfluous-parens
# pylint: disable=bare-except
"""
### Checks if FFmpeg is installed and added to path, or if ffmpeg.exe can be found in the current directory. Otherwise, downloads it.
"""

import os
import re
import zipfile
import subprocess
import requests


def download_ffmpeg():
    """
    ### Args
    - None

    ### Returns
    - None

    ### Errors raised
    - None
    """
    regex = r"ffmpeg.*.zip"
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-06-30-12-38/ffmpeg-n4.4-78-g031c0cb0b4-win64-gpl-4.4.zip"
    # Finds the name of the zip and cuts off the .zip part
    name_of_zip = re.search(regex, url).group()[:-4]
    open("ffmpeg.zip", "wb").write(requests.get(url, allow_redirects=True).content)
    with zipfile.ZipFile("ffmpeg.zip", "r") as ffmpeg_zip:
        ffmpeg_zip.extract(f"{name_of_zip}/bin/ffmpeg.exe")

    # Clean up after extracting the zip file
    os.replace(f"{name_of_zip}/bin/ffmpeg.exe", "./ffmpeg.exe")
    os.remove("ffmpeg.zip")
    try:
        os.remove(f"{name_of_zip}/bin/ffmpeg.exe")
    except:
        print(f"{name_of_zip}/bin/ffmpeg.exe already deleted, moving on...")
    os.rmdir(f"{name_of_zip}/bin")
    os.rmdir(f"{name_of_zip}")


try:
    devnull = open(os.devnull)
    subprocess.Popen(["ffmpeg"], stdout=devnull, stderr=devnull).communicate()
    print("Found ffmpeg in PATH!")
except OSError as e:
    if not os.path.isfile("./ffmpeg.exe"):
        print("ffmpeg not found, downloading it...")
        download_ffmpeg()
