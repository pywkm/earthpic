from setuptools import setup

setup(
    name='earthpic',
    version='0.1',
    packages=['earthpic', 'earthpic.tests'],
    url='',
    license='BSD',
    author='Wiktor Matuszewski',
    author_email='pywkm@wukaem.pl',
    description=(
        'Downloading Earth photos from http://himawari8.nict.go.jp made easy'
    ),
    entry_points={
        'console_scripts': [
            'earthpic = earthpic.earth:main',
        ],
    },
    requires=['pytz', 'requests', 'Pillow', 'click'],
)
