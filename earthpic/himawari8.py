#!/usr/bin/env python3
"""
docstring
"""

import itertools
import logging
import shutil
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

from .constants import CWD
from .utils import round_time

logger = logging.getLogger(__name__)


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
        1: 'xs',
        2: 'small',
        4: 'big',
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
        self._blank_image_path = Path(CWD).parent / 'bin' / 'blank_image.png'
        self._prepare_files()
        self._blank_image = Image.open(self._blank_image_path)
        self._session = requests.Session()
        self.scale = scale
        self.time = round_time() - timedelta(minutes=self.delay)

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

    def _prepare_files(self):
        if not self._images_path.exists():
            Path.mkdir(self._images_path)

        if not self._blank_image_path.exists():
            self._create_blank_image()

    def _create_blank_image(self):
        near_future = round_time() + timedelta(hours=1)
        url = self._get_url(near_future, scale=1)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(str(self._blank_image_path), 'wb') as fout:
                shutil.copyfileobj(response.raw, fout)
        del response

    def fetch_one(self, time=None, scale=None):
        if time:
            self.time = time
        if scale:
            self.scale = scale

        fpath = self._get_file_path()
        if fpath.exists():
            logger.info('Image already downloaded')

            return str(fpath)

        self._save_image(fpath)

    def _save_image(self, fpath):
        png = Image.new(
            'RGB',
            (self.tsize * self.scale, self.tsize * self.scale),
        )
        for x, y in itertools.product(range(self.scale), range(self.scale)):
            tiledata = self._download_tile(x, y)
            tile = Image.open(BytesIO(tiledata))
            if tile == self._blank_image:
                logger.info('No Earth image at given time. File not saved.')
                return
            png.paste(tile, (self.tsize * x, self.tsize * y))
        png.save(str(fpath), 'PNG')
        logger.info('Image saved as: {}'.format(fpath))
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
        logger.info("Fetching tile: {}".format(path))
        try:
            return self._session.get(path).content
        except requests.ConnectionError:
            logger.info('Connection Error. Retrying.')
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
