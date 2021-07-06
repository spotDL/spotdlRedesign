"""
### Checks if FFmpeg is installed and added to path, or if ffmpeg.exe can be found in the current directory. Otherwise, downloads it.
"""

import platform
import os
import shutil
import stat
from pathlib import Path
import subprocess
import re
import requests


def download_ffmpeg():
    """
    ### Args
    - None

    ### Returns
    - Path of the downloaded binary

    ### Errors raised
    - OS or Architecture not detected
    - FFmpeg failed to download
    """

    sources = {
        # !I used platform.machine() to find these values.
        # !The 32bit values & Darwin's are educated guesses, as I do not have any 32bit machines
        # !Or any macOS devices.
        "windows": {
            "amd64": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/win32-x64",
            "i686": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/win32-ia32",
        },
        "linux": {
            "x86_64": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/linux-x64",
            "x86": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/linux-ia32",
            "arm32": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/linux-arm",
            "aarch64": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/linux-arm64",
        },
        "darwin": {
            "x86_64": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/darwin-x64",
            "x86": "https://lame.buanzo.org/ffmpeg-mac-2.2.2.zip",
            "arm": "https://github.com/eugeneware/"
            "ffmpeg-static/releases/download/b4.4/darwin-arm64",
        },
    }

    os_name = platform.system().lower()
    os_arch = platform.machine().lower()

    link_to_use = sources.get(os_name, {}).get(os_arch)
    if link_to_use is None:
        raise Exception(
            "Could not detect architecture or operating system. "
            "Please submit an issue on this project's GitHub page."
        )
    current_dir = os.path.dirname(__file__)
    ffmpeg_data = requests.get(link_to_use, allow_redirects=True).content

    # !create "ffmpeg.exe" on windows and "ffmpeg" on other platforms 
    ffmpeg_exec = Path(
        f"{current_dir}/defaults/misc/ffmpeg" + (".exe" if os_name == "windows" else "")
    )
    with open(ffmpeg_exec, "wb") as file:
        file.write(ffmpeg_data)
    if ffmpeg_exec.exists() is not True:
        raise Exception(
            "FFmpeg failed to download. "
            "Please try again or create an Issue on GitHub."
        )
    if os_name in ["linux", "darwin"]:
        ffmpeg_exec.chmod(ffmpeg_exec.stat().st_mode | stat.S_IEXEC)
    return ffmpeg_exec


def check_ffmpeg():
    """
    ### Args
    - None

    ### Returns
    - True if FFmpeg is found on PATH or in the directory where it gets downloaded
    - False if: FFmpeg is not found on PATH OR the version is not compatible

    ### Errors raised
    - None
    """
    regex = r"[0-9]\.[0-9]"

    if shutil.which("ffmpeg") is not None:
        test_str = str(subprocess.check_output(["ffmpeg", "-version"]))
        ffmpeg_version = re.search(regex, test_str).group()
        if ffmpeg_version < 4.4:
            print(f"FFmpeg version is not > or = to 4.2 . You have {ffmpeg_version}")
            return False
        else:
            return True
    else:
        os_name = platform.system().lower()
        current_dir = os.path.dirname(__file__)
        ffmpeg_exec = Path(
            f"{current_dir}/defaults/misc/ffmpeg"
            + (".exe" if os_name == "windows" else "")
        )
        return bool(ffmpeg_exec.exists())
