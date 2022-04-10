from setuptools import setup, find_packages

requires = [
    'Brotli'
    'certifi'
    'charset-normalizer'
    'click'
    'Flask'
    'gunicorn'
    'idna'
    'importlib-metadata'
    'itsdangerous'
    'Jinja2'
    'MarkupSafe'
    'mutagen'
    'pycryptodomex'
    'requests'
    'six'
    'spotipy'
    'urllib3'
    'websockets'
    'Werkzeug'
    'youtube-search'
    'yt-dlp'
    'zipp'
]

setup(
    name='TrackDown',
    version='1.0',
    description='An application that gets your Spotify songs and downloads the YoutubeMP3 version',
    author='Het Patel',
    author_email='het1613@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)