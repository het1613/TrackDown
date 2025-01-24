# TrackDown
![Demo](https://github.com/het1613/TrackDown/blob/master/static/photos/screenshots/demo.gif?raw=true)

## Inspiration

TrackDown is a MP3 converter web app that leverages Spotify Web API and several Python YouTube related libraries to automatically retrieve your playlists on Spotify and download their corresponding MP3 files from YouTube.

Having an older car without Bluetooth can be a struggle, especially since you can't link your phone and listen from your Spotify account. As such, since most cars have USB ports or something similar, you can individually download each song from YouTube. However, if you have hundreds of tracks, this can become tedious and frustrating. There are other mass converters; however, they don't often download the correct songs from YouTube.

This led me to creating TrackDown. With this app, you can easily automate the process of going through your Spotify playlist, finding the song on YouTube and downloading its MP3 file.

## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/): Web framework used for setting up the app backend

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/): Used to retrieve user data such as their playlists

- [Python (Requests)](https://docs.python-requests.org/en/master/): Used for sending requests to the Spotify Web API with Python

- [youtube_search](https://pypi.org/project/youtube-search/): Used for YouTube queries

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): Used to download MP3 file of YouTube video

- [Heroku](https://dashboard.heroku.com/apps): Platform used to deploy the app

## Getting Started

1. Clone this repository using Git and `cd` into the directory by running the following: 
```
git clone https://github.com/het1613/TrackDown.git
cd TrackDown
python -m venv env
source env/bin/activate
```
        
2. Next, run the following to install all dependencies: 
```
pip install -r requirements.txt
```
        
3. Create a [Spotify Dev account](https://developer.spotify.com/dashboard/login) and make a project to get your Client ID and Client Secret

4. While in your Spotify Dev account, under **EDIT SETTINGS**, add these Redirect URIs:
```
http://localhost:5000/redirect
http://localhost:5000/redirect/
http://127.0.0.1:5000/redirect
http://127.0.0.1:5000/redirect/
```

5. Create a new **".env"** file and add the following:
```
CLIENT_ID=CLIENT_ID
CLIENT_SECRET=CLIENT_SECRET
```

6. Install ffmeg on your machine:

Mac: `brew install ffmeg`

Linux: `sudo apt-get install ffmeg`

Windows: `choco install ffmeg` (make sure you have [Chocolatey](https://chocolatey.org/install) installed and run the command in CMD as administrator)

7. Finally, run the web app locally:
```
python app.py
```

## Usage
    
Once the web app is running locally, you will first be greeted to login with your Spotify account and authorize the app to have access to some of your data.

![Login Page](https://github.com/het1613/TrackDown/blob/master/static/photos/screenshots/login%20page.png?raw=true)

Once logged in, you can see your profile and the navigation bar to download your playlists.

![Home Page](https://github.com/het1613/TrackDown/blob/master/static/photos/screenshots/home.png?raw=true)

Under the **Download My Music** tab, you can see all your saved songs and playlists. Choose any one of them that you'd like to download.

![Playlists Page](https://github.com/het1613/TrackDown/blob/master/static/photos/screenshots/playlists.png?raw=true)

After choosing a playlist, you can see all the songs you can download. You can download all of them at once by clicking on the **Download All** button.

![Playlist Page](https://github.com/het1613/TrackDown/blob/master/static/photos/screenshots/playlist.png?raw=true)

![Downloading](https://github.com/het1613/TrackDown/blob/master/static/photos/screenshots/downloading.png?raw=true)

Finally, traverse to your `Downloads/{Playlist Name}` folder to see your downloaded MP3 files.

![Downloading](https://github.com/het1613/TrackDown/blob/master/static/photos/screenshots/saved.png?raw=true)

## Authors

- **Het Patel** - [het1613](https://github.com/het1613)
