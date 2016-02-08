#!/usr/bin/env python3
"""
docstring
"""
import ctypes
# import os
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image

import pytz

from .constants import CWD

cwd = CWD  # os.path.dirname(os.path.abspath(__file__))


SPI_SETDESKWALLPAPER = 20  # 0x14
SPIF_UPDATEINIFILE = 3  # 0x1


def round_time(dtime=None, round_to=600):
    """Floor round a datetime object to any time laps in seconds.
    If not specified, treats datetime object as in UTC timezone.
    @param dtime: datetime object or None. If None, returns rounded current time
    @param round_to: time laps in seconds (default: 600s = 10min)
    """
    # print(dtime)
    tz = pytz.utc
    if dtime is None:
        dtime = datetime.now(tz)
    # print(dtime)
    if not dtime.tzinfo:
        dtime = tz.localize(dtime)
    # print(dtime)
    # if (dtime.minute*60 + dtime.second) % round_to == 0:
    #     print(dtime.second)
    #     return dtime - timedelta(microseconds=-dtime.microsecond)
    seconds = (dtime - datetime(1970, 1, 1, tzinfo=tz)).seconds
    rounding = (seconds // round_to) * round_to
    # print(seconds, rounding)
    return dtime + timedelta(0, rounding - seconds, -dtime.microsecond)


def set_wallpaper(file_path):
    temp_file = str(Path(CWD).parent / 'bin' / 'wallpaper.bmp')
    im = Image.open(file_path)
    im.save(temp_file)
    print('setting wallpaper:', temp_file)
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        1,
        temp_file,
        SPIF_UPDATEINIFILE,
    )
