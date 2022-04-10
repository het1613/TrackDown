from flask import Flask, render_template, request, url_for, session, redirect
import spotipy, time
from spotipy.oauth2 import SpotifyOAuth
import downloadMP3

app = Flask(__name__)

app.secret_key = "hkb34hvhj3vbjh4IEVIv4ivb"
app.config['SESSION_COOKIE_NAME'] = 'TrackDown Cookie'
TOKEN_INFO = "token_info"

clientID     = "ADD YOUR CLIENT ID HERE"
clientSecret = "ADD YOUR CLIENT SECRET HERE"

@app.route('/')
def login():
    oauth = create_spotify_oauth()
    auth_url = oauth.get_authorize_url()
    return render_template("login.html", url=auth_url)

@app.route('/redirect')
def redirectPage():
    oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('home', _external=True))

@app.route('/home')
def home():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for('login', _external=True))

    sp = spotipy.Spotify(auth=token_info['access_token'])

    userData = sp.current_user()
    userName = userData["display_name"]
    userFollowers = userData["followers"]["total"]
    userDP = userData["images"][0]["url"] if len(userData["images"]) != 0 else None

    userFollowing = len(sp.current_user_followed_artists(limit=50)['artists']['items'])
    userNumofPlaylists = len(sp.current_user_playlists(limit=50)['items'])

    return render_template("home.html", name=userName, followers=userFollowers, following=userFollowing, dp=userDP, playlists=userNumofPlaylists+1)

@app.route('/playlists')
def playlists():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for('login', _external=True))

    sp = spotipy.Spotify(auth=token_info['access_token'])

    data = sp.current_user_playlists(limit=50)['items']
    playlists = []
    
    if data:
        for playlist in data:
            info = {'name':playlist['name'], 'id':playlist['id'], 'total':playlist['tracks']['total']}
            
            if playlist['images'] != []:
                info['cover'] = playlist['images'][0]['url']
            
            else:
                info['cover'] = None

            playlists.append(info)

    return render_template("playlists.html", playlists=playlists)

@app.route('/playlists/<id>', methods=["POST", "GET"])
def chosenPlaylist(id):
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for('login', _external=True))

    sp = spotipy.Spotify(auth=token_info['access_token'])

    all_songs = []
    iteration = 0

    while True:
        if (id == "saved-songs"):
            current_songs = sp.current_user_saved_tracks(limit=50, offset=iteration*50)['items']
        else:
            current_songs = sp.playlist_items(playlist_id=id, limit=50, offset=iteration*50)['items']

        iteration += 1

        for item in current_songs:

            if 'track' in item:
                track = item['track']
            else:
                track = item
    
            try:
                track_name = track['name']
                track_artist = track['artists'][0]['name']
                value = f"{track_name} - {track_artist}"
                all_songs.append(value)

            except KeyError:
                print('Skipping track')

        if len(current_songs) < 50:
            break
    
    if id == "saved-songs":
        playlist_cover = url_for('static', filename='photos/saved_songs.png')
    
    else:
        playlist_cover = sp.playlist_cover_image(playlist_id=id)[0]['url']

    if playlist_cover == None:
        playlist_cover = url_for('static', filename='photos/blank_cover.png')
    
    if id == "saved-songs":
        name = "Liked Songs"
    
    else:
        data = sp.current_user_playlists(limit=50)['items']

        for playlist in data:
            if playlist['id'] == id:
                name = playlist['name']
                break
        else:
            name = 'Playlist'

    if request.method == "POST":
        downloadMP3.ListToMP3(playlist_name=name, playlist_songs=all_songs)
    
    return render_template("chosenPlaylist.html", all_songs=enumerate(all_songs), name=name, cover=playlist_cover)

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login', _external=True))

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60

    if is_expired:
        oauth = create_spotify_oauth()
        token_info = oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=clientID,
        client_secret=clientSecret,
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-read-private user-follow-read playlist-read-private playlist-read-collaborative"
    )