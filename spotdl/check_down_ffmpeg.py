"""
### Checks if FFmpeg is installed and added to path, or if ffmpeg.exe can be found in the current directory. Otherwise, downloads it.
"""

import platform
import os
import shutil
import stat
from pathlib import Path
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

    link_to_use = sources[os_name][os_arch]
    if link_to_use is None:
        raise Exception(
            "Could not detect architecture or operating system. "
            "Please submit an issue on this project's GitHub page."
        )
    current_dir = os.path.dirname(__file__)
    ffmpeg_data = requests.get(link_to_use, allow_redirects=True).content

    ffmpeg_exec = Path(
        f"{current_dir}/ffmpeg/bin/ffmpeg" + ".exe" if os_name == "windows" else ""
    )
    with open(ffmpeg_exec, "wb") as file:
        file.write(ffmpeg_data)
    if os_name in ["linux", "darwin"]:
        ffmpeg_exec.chmod(ffmpeg_exec.stat().st_mode | stat.S_IEXEC)


def check_ffmpeg():
    """
    ### Args
    - None

    ### Returns
    - True if FFmpeg is found on PATH

    ### Errors raised
    - False if FFmpeg is not found on PATH
    """
    return bool(shutil.which("ffmpeg") is not None)
