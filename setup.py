try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='robohash',
    packages=['robohash'],
    version='1.0',
    description='One of the leading robot-based hashing tools on the web',
    long_description=long_description,
    author='Colin Davis',
    author_email='colin@robohash.org',
    url='https://github.com/e1ven/Robohash',
    download_url='https://github.com/e1ven/Robohash/tarball/1.0',
    keywords=['robots'], # arbitrary keywords
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
    ],
    package_data={
        'robohash': [
            'sets/set1/*/*/*',
            'sets/set2/*/*',
            'sets/set3/*/*',
            'sets/set4/*/*',
            'sets/set5/*/*',
            'backgrounds/*/*',
        ]
    },
    install_requires=['pillow', 'natsort'],
    extras_require={
        'web': ['tornado'],
    },
)
