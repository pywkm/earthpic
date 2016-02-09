earthpic
========

Python script downloading Earth photos taken by Himawari-8 satelite.
Website: http://himawari8.nict.go.jp/

Inspired by this reddit thread:
https://www.reddit.com/r/programming/comments/441do9/i_made_a_windows_powershell_script_that_puts_a/

Especially by european_impostor's Powershell script:
https://gist.github.com/MichaelPote/92fa6e65eacf26219022

And most of all, its Python implementations:
by celoyd: https://gist.github.com/celoyd/39c53f824daef7d363db
and by willwhitney: https://gist.github.com/willwhitney/e9e2c42885385c51843e

This script is Windows specific. Python 3.4+ only compatible.
Tested on Windows 7, Python 3.4.4 and Python 3.5.1

Installation
------------
To install, download source or clone it with git

    git clone https://github.com/pywkm/earthpic.git


Change to eartpic/ directory and run setup.py

    cd earthpic/
    python setup.py install


If you have problem with installing Pillow package with `pip install pillow`
you can download wheel file from http://www.lfd.uci.edu/~gohlke/pythonlibs/
and install it with command `pip install <path/to/whl_file>`

Usage
-----
Call `earthpic --help` from command line to view this help:

    usage: earthpic [-h] [-d DATE] [-t TIME] [-s SCALE] [-w] [-v] [-l N_PHOTOS]
                    [-b] [-p PATH]

    Download satelite Earth photo(s)

    optional arguments:
      -h, --help            show this help message and exit
      -d DATE, --date DATE  date of the photo [format: YYYY-MM-DD] (default:
                            2016-02-09)
      -t TIME, --time TIME  time of the photo [fotmat: hh:mm] (default: 00:05)
      -s SCALE, --scale SCALE
                            scale of the photo, choices: 1, 2, 4, 8, 16 or 20
                            (default: 2)
      -w, --wallpaper       set downloaded image as desktop wallpaper (default:
                            False)
      -v, --verbose         increase output verbosity (default: False)
      -l N_PHOTOS, --last N_PHOTOS
                            process N photos to given date (default: 1)
      -b, --batch           run batch downloading photos. To stop, press ctrl+c.
                            (default: False)
      -p PATH, --path PATH  path where images will be saved (default: images)

