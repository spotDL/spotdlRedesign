"""
### Checks if FFmpeg is installed and added to path, or if ffmpeg.exe can be found in the current directory. Otherwise, downloads it.
"""

import platform
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

    windows_url_64 = ("https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-06-30-12-38/" +
    "ffmpeg-n4.4-78-g031c0cb0b4-win64-gpl-4.4.zip")
    windows_url_32 = "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/win32-ia32.gz"
    linux_url_amd64 = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz"
    linux_url_arm64 = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-arm64-static.tar.xz"
    linux_url_arm32 = "https://github.com/bravobit/FFmpeg-Android/raw/master/android-ffmpeg/src/main/assets/x86/ffmpeg"
    linux_url_i686 = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-i686-static.tar.xz"
    mac_url_64 = "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/darwin-x64.gz"
    mac_url_32 = "https://lame.buanzo.org/ffmpeg-mac-2.2.2.zip"
    mac_url_arm = "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/darwin-arm64.gz"

    # Check the OS and Architecture of the user, then use appropriate link.
    # I am not sure if all of these cases are accurate, more testing is required.
    if platform.architecture()[0] == "64bit":
        if platform.system == "Windows":
            to_use_url = windows_url_64
        elif platform.system == "Linux":
            # Since Desktop linux and Android both return "Linux", we need to do an additional check
            if platform.uname().machine == "x86_64":
                #Desktop Linux
                to_use_url = linux_url_amd64
            elif platform.uname().machine == "aarch64":
                #Android
                to_use_url = linux_url_arm64
            else:
                raise Exception("Could not detect architecture." +
                " Please submit an issue on GitHub containing your system information.")
        elif platform.system == "Darwin":
            if platform.machine == "arm":
                to_use_url = mac_url_arm
            elif platform.machine == "x86_64":
                to_use_url = mac_url_64
            else:
                raise Exception("Could not detect architecture." +
                " Please submit an issue on GitHub containing your system information.")
    elif platform.architecture()[0] == "32bit":
        if platform.system == "Windows":
            to_use_url = windows_url_32
        elif platform.system == "Linux":
            # Since Desktop linux and Android both return "Linux", we need to do an additional check.
            # I don't know and I have no way of testing if this is accurate.
            # These are just educated guesses.
            if platform.uname().machine == "i386":
                #Desktop Linux
                to_use_url = linux_url_i686
            elif platform.uname().machine == "x86":
                #Android
                raise Exception("Sorry, 32-bit android is not supported by FFmpeg.")
            else:
                raise Exception("Could not detect architecture." +
                " Please submit an issue on GitHub containing your system information.")
        elif platform.system == "Darwin":
            to_use_url = mac_url_32

    # TODO Create extract function for each architecture

try:
    # I cannot explain, this snippet of code is from Stack Overflow and I do not understand it.
    devnull = open(os.devnull)
    subprocess.Popen(["ffmpeg"], stdout=devnull, stderr=devnull).communicate()
    print("Found ffmpeg in PATH!")
except OSError as e:
    if not os.path.isfile("./ffmpeg.exe"):
        print("ffmpeg not found, downloading it...")
        download_ffmpeg()
