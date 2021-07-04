"""
### Checks if FFmpeg is installed and added to path, or if ffmpeg.exe can be found in the current directory. Otherwise, downloads it.
"""

import platform
import os
import shutil
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

    sources = {
        # !I used platform.machine() to find these values.
        # !The 32bit values & Darwin's are educated guesses, as I do not have any 32bit machines
        # !Or any macOS devices.
        "Windows": {
            "AMD64":    "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/win32-x64",
            "i686":     "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/win32-ia32",
            "arm":      "PUT SOMETHING HERE!!!!"
        },
        "Linux": {
            "x86_64":   "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-x64",
            "x86":      "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-ia32",
            "arm32":    "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-arm",
            "aarch64":  "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-arm64"
        },
        "Darwin": {
            "x86_64":   "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/darwin-x64",
            "x86":      "https://lame.buanzo.org/ffmpeg-mac-2.2.2.zip",
            "arm":      "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/darwin-arm64"
        }
    }

    try:
        link_to_use = sources[platform.system()][platform.machine()]
    except:
        # Should change this message once we know for sure the output of the previous command
        # On any and all OS and Architectures listed.
        raise Exception("Could not detect architecture or operating system. "
                        "Please open an issue on the GitHub page of this project.")
    current_dir = os.path.dirname(__file__)
    ffmpeg_data = requests.get(link_to_use, allow_redirects=True).content
    if link_to_use == sources["Darwin"]["x86"]:
        print("")
        # TODO make functionality for this case
    elif platform.system() == "Windows":
        open(f"{current_dir}\\ffmpeg\\bin\\ffmpeg.exe", "wb").write(ffmpeg_data)
    else:
        open(f"{current_dir}/ffmpeg/bin/ffmpeg", "wb").write(ffmpeg_data)

if shutil.which("ffmpeg") is not None:
    print("Found ffmpeg in path. No need to download!")
else:
    print("Could not find ffmpeg in the path. Downloading it, please be patient...")
    download_ffmpeg()