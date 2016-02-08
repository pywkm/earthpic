#!/usr/bin/env python3
"""
Main console script
"""

import argparse
import logging
import sched
import time
from datetime import datetime, timedelta

import pytz

from earthpic.himawari8 import EarthPhoto
from earthpic.utils import (
    set_wallpaper,
    info_console_handler,
    debug_console_handler,
)

logger = logging.getLogger(__name__)

s = sched.scheduler(time.time, time.sleep)


def scheduled(earth_photo, sc):
    now = datetime.now(pytz.utc)
    print(now)
    pic = earth_photo.fetch_one(now - timedelta(minutes=20))
    if pic:
        set_wallpaper(pic)
    sc.enter(600, 1, scheduled, (earth_photo, sc))


start_time = datetime.now(pytz.utc) - timedelta(minutes=20)
default_date = start_time.strftime('%Y-%m-%d')
default_time = start_time.strftime('%H:%M')

parser = argparse.ArgumentParser(
    prog='earthpic',
    description='Download satelite Earth photo(s)',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    '-d',
    dest='date',
    metavar='DATE',
    default=default_date,
    help='date of the photo [format: YYYY-MM-DD]',
)
parser.add_argument(
    '-t',
    dest='time',
    metavar='TIME',
    default=default_time,
    help='time of the photo [fotmat: hh:mm]',
)
parser.add_argument(
    '-s',
    dest='scale',
    type=int,
    metavar='SCALE',
    choices=(1, 2, 4, 8, 16, 20),
    default=2,
    help='scale of the photo, choices: 1, 2, 4, 8, 16 or 20'
)
parser.add_argument(
    '-w',
    '--wallpaper',
    help='set downloaded image as desktop wallpaper',
    action='store_true',
)
parser.add_argument(
    '-v',
    '--verbose',
    help='increase output verbosity',
    action='store_true',
)
parser.add_argument(
    '--debug',
    action='store_true',
    help=argparse.SUPPRESS,
)


def main():
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().addHandler(info_console_handler)
    if args.debug:
        logging.getLogger().addHandler(debug_console_handler)

    logger.debug(args)

    if args.scale > 4:
        answer = input(
            'Are you sure you want to download photo of that size '
            '({0}x{0}={1} tiles)?'.format(args.scale, args.scale ** 2) +
            ' [Y/n] '
        )
        if answer.lower() in ('n', 'no'):
            return
    earth_photo = EarthPhoto(args.scale)

    date_string = '{} {}'.format(args.date, args.time)
    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    date = pytz.utc.localize(date)
    if date > start_time:
        date = start_time

    logger.debug(date)
    logger.debug(start_time)

    image_path = earth_photo.fetch_one(date)
    if args.wallpaper:
        set_wallpaper(image_path)

        # s.enter(1, 1, scheduled, (earth_photo, s))
        # s.run()

        # pic = earth_photo.fetch_one()
        # set_wallpaper(pic)
        # earth_photo.fetch_many(datetime.now(pytz.utc) - timedelta(hours=12))


if __name__ == "__main__":
    main()
