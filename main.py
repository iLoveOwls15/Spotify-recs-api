import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth 
from dotenv import load_dotenv
load_dotenv()

#load spotify auth manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth( 
    client_id=os.getenv("CLIENT_ID"), 
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URL"),
    scope="user-top-read playlist-modify-public"
))

def find_recs(): 
    top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=5)  
    seed_track_ids = [track['id'] for track in top_tracks['items']]  #collecting track ids

    tracks = []
    while len(tracks) < 9999:  #fetch till 9999
        recs = sp.recommendations(seed_tracks=seed_track_ids[:5], limit=5)  #5 seed limit 
        tracks.extend([track['id'] for track in recs['tracks']])  #rec track ids
    tracks = tracks[:9999] #max 9999 tracks due to limit

    #create playlist
    user_id = sp.me()['id']  # Get the current user's ID
    playlist = sp.user_playlist_create(user=user_id, name="9999 Song Recs", public=True)
    #100 songs per pull request
    for i in range(0, len(tracks), 100):
        sp.user_playlist_add_tracks(user_id, playlist['id'], tracks[i:i+100])
        time.sleep(1) #VERY IMPORTANT

    print(f"playlist created")

if __name__ == "__main__":
    find_recs()
