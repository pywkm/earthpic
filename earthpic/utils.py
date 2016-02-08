#!/usr/bin/env python3
"""
Usefull utilities
"""
import ctypes
import logging
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image

import pytz

from .constants import CWD

# logging object:
logger = logging.getLogger(__name__)

# create console handlers and set levels
info_console_handler = logging.StreamHandler()
info_console_handler.setLevel(logging.INFO)
debug_console_handler = logging.StreamHandler()
debug_console_handler.setLevel(logging.DEBUG)

# create formatters
formatter = logging.Formatter('%(levelname)s: %(message)s')
formatter2 = logging.Formatter('%(name)18s: (%(levelname)s) %(message)s')

# add formatters
info_console_handler.setFormatter(formatter)
debug_console_handler.setFormatter(formatter2)

# WinAPI constants
SPI_SETDESKWALLPAPER = 20  # 0x14
SPIF_UPDATEINIFILE = 3


def round_time(dtime=None, round_to=600):
    """Floor round a datetime object to any time laps in seconds.
    If not specified, treats datetime object as in UTC timezone.
    @param dtime: datetime object or None. If None, returns rounded current time
    @param round_to: time laps in seconds (default: 600s = 10min)
    """
    tz = pytz.utc
    logger.debug('In round_time (dtime 1): {}'.format(dtime))
    if dtime is None:
        dtime = datetime.now(tz)
    logger.debug('In round_time (dtime 2): {}'.format(dtime))
    if not dtime.tzinfo:
        dtime = tz.localize(dtime)
    logger.debug('In round_time (dtime 3): {}'.format(dtime))
    seconds = (dtime - datetime(1970, 1, 1, tzinfo=tz)).seconds
    rounding = (seconds // round_to) * round_to
    logger.debug('seconds: {} rounding: {}'.format(seconds, rounding))
    dtime = dtime + timedelta(0, rounding - seconds, -dtime.microsecond)
    logger.debug('In round_time (dtime 4): {}'.format(dtime))
    return dtime


def set_wallpaper(file_path):
    temp_file = str(Path(CWD).parent / 'bin' / 'wallpaper.bmp')
    im = Image.open(file_path)
    im.save(temp_file)
    logger.info('Setting wallpaper: {}'.format(temp_file))
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        temp_file,
        SPIF_UPDATEINIFILE,
    )
