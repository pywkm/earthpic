#!/usr/bin/env python3
"""
docstring
"""

import itertools
import os
import shutil
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path

import pytz
import requests
from PIL import Image

from .utils import round_time
from .constants import CWD

# cwd = os.path.dirname(os.path.abspath(__file__))


class EarthPhoto:
    url_pattern = (
        'http://himawari8.nict.go.jp/img/D531106/{scale}d/550/'
        '{year}/{month:02}/{day:02}/{hour:02}{min:02}00_{x}_{y}.png'
    )
    filename_pattern = (
        'earth_{year}-{month:02}-{day:02}_{hour:02}-{min:02}_{size}.png'
    )
    tsize = 550
    sizes = {
        1: 'xxs',
        2: 'xs',
        4: 'small',
        8: 'large',
        16: 'xl',
        20: 'xxl',
    }
    delay = 20  # in minutes

    def __init__(self, scale=2, storage_path=None):
        if storage_path:
            self._images_path = Path(storage_path)
        else:
            self._images_path = Path(CWD).parent / 'images'
        self._no_img_path = Path(CWD).parent / 'bin' / 'no_image_tile.png'
        self._sess = requests.Session()
        self.scale = scale
        self.time = round_time() - timedelta(minutes=self.delay)
        self._setup()
        self._no_image = Image.open(self._no_img_path)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        try:
            self.sizes[scale]
        except KeyError:
            raise ValueError('Scale must be an integer: 1, 2, 4, 8, 16 or 20')
        self._scale = scale

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = round_time(value)

    def _setup(self):
        if not self._images_path.exists():
            Path.mkdir(self._images_path)

        if not self._no_img_path.exists():
            near_future = datetime.now() + timedelta(hours=1)
            time = round_time(near_future)
            url = self._get_url(time, scale=1)
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(str(self._no_img_path), 'wb') as fout:
                    shutil.copyfileobj(response.raw, fout)
            del response

    def fetch_one(self, time=None, scale=None):
        if time:
            self.time = time
        if scale:
            self.scale = scale
        fpath = self._get_file_path()
        if fpath.exists():
            print('Image already downloaded')
            return str(fpath)

        png = Image.new('RGB',
                        (self.tsize * self.scale, self.tsize * self.scale))

        for x, y in itertools.product(range(self.scale), range(self.scale)):
            tiledata = self._download_tile(x, y)
            tile = Image.open(BytesIO(tiledata))
            if tile == self._no_image:
                print('No Earth image at given time. File not saved.')
                return
            png.paste(tile, (self.tsize * x, self.tsize * y))

        png.save(str(fpath), 'PNG')
        print('Image saved as:\n{}'.format(fpath))
        return str(fpath)

    def fetch_many(self, start_time, end_time=None, scale=2):
        time = round_time(start_time)
        if end_time:
            end_time = round_time(end_time)
        else:
            end_time = round_time() - timedelta(minutes=self.delay)
        while time <= end_time:
            self.fetch_one(time, scale)
            time += timedelta(minutes=10)

    def _download_tile(self, x, y):
        path = self._get_url(x=x, y=y)
        print("fetching {}".format(path))
        try:
            return self._sess.get(path).content
        except requests.ConnectionError:
            print('Connection Error. Retrying.')
            return self._download_tile(x, y)

    def _params(self, time=None, scale=None):
        time = time if time else self.time
        scale = scale if scale else self.scale
        return dict(
            scale=scale,
            year=time.year,
            month=time.month,
            day=time.day,
            hour=time.hour,
            min=time.minute,
        )

    def _get_url(self, time=None, scale=None, x=0, y=0):
        return self.url_pattern.format(
            **self._params(time, scale),
            x=x,
            y=y,
        )

    def _get_file_path(self):
        return self._images_path / self.filename_pattern.format(
            **self._params(),
            size=self.sizes[self.scale],
        )


def main():
    earth_photo = EarthPhoto()
    # earth_photo.fetch_one(datetime.now(pytz.utc)-timedelta(hours=24))
    # earth_photo.fetch_one(datetime.now(pytz.utc)-timedelta(minutes=30), scale=8)
    # earth_photo.fetch_one(datetime(2016, 2, 5, 2, 50), scale=20)
    # earth_photo.fetch_one()
    earth_photo.fetch_many(datetime.now(pytz.utc) - timedelta(hours=12))


if __name__ == '__main__':
    main()
