from distutils.core import setup

with open('README.txt') as file:
    long_description = file.read()

setup(
    name = 'robohash',
    packages = ['robohash'], 
    version = '1.0',
    description = 'One of the leading robot-based hashing tools on the web',
    long_description=long_description,
    author = 'Colin Davis',
    author_email = 'cdavis@tavern.is',
    url = 'https://github.com/e1ven/Robohash',
    download_url = 'https://github.com/e1ven/Robohash/tarball/1.0',
    keywords = ['robots'], # arbitrary keywords
    classifiers = [],
)