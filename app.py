import os
from flask import Flask, render_template, redirect, url_for, request, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Spotipy with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope='user-library-read playlist-read-private playlist-read-collaborative'
))

@app.route('/')
def home():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    sp.token = session['token']
    user_data = sp.current_user()
    playlists_data = sp.current_user_playlists()
    
    return render_template('home.html', user_data=user_data, playlists=playlists_data['items'])

@app.route('/login')
def login():
    if 'token' in session:
        return redirect(url_for('home'))
    
    return redirect(sp.auth_manager.get_authorize_url())

@app.route('/callback')
def callback():
    token_info = sp.auth_manager.get_access_token(request.args.get('code'))
    session['token'] = token_info['access_token']
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('home'))

@app.route('/playlists')
def playlists():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    sp.token = session['token']
    playlists = sp.current_user_playlists()
    
    return render_template('playlists.html', playlists=playlists['items'])

@app.route('/playlist/<playlist_id>')
def playlist(playlist_id):
    if 'token' not in session:
        return redirect(url_for('login'))
    
    sp.token = session['token']
    playlist = sp.playlist_tracks(playlist_id)
    
    return render_template('playlist.html', playlist=playlist['items'], playlist_id=playlist_id)

@app.route('/profile')
def profile():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    sp.token = session['token']
    user_data = sp.current_user()
    
    return render_template('profile.html', user_data=user_data)


@app.route('/play_song/<track_id>')
def play_song(track_id):
    if 'token' not in session:
        return redirect(url_for('login'))
    
    track_url = sp.track(track_id)['external_urls']['spotify']
    return redirect(track_url)

@app.route('/leave_thought', methods=['POST'])
def leave_thought():
    thought = request.form.get('thought')
    # Handle storing the thought in the database or other processing
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
