import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        """Initialize the Spotify client with proper authentication."""
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-top-read playlist-modify-public user-library-read"
        ))
        self.user_id = self.sp.me()['id']
    
    def get_top_tracks(self, time_range='medium_term', limit=5):
        """Get user's top tracks."""
        top_tracks = self.sp.current_user_top_tracks(time_range=time_range, limit=limit)
        return top_tracks['items']
    
    def create_recommendations_playlist(self, name="Song Recommendations", max_tracks=100):
        """Create a playlist with recommendations based on top tracks."""
        # Get seed tracks
        top_tracks = self.get_top_tracks(limit=5)
        seed_track_ids = [track['id'] for track in top_tracks]
        
        # Get recommendations
        tracks = []
        while len(tracks) < max_tracks:
            recs = self.sp.recommendations(seed_tracks=seed_track_ids[:5], limit=min(100, max_tracks - len(tracks)))
            new_track_ids = [track['id'] for track in recs['tracks']]
            tracks.extend(new_track_ids)
            if len(new_track_ids) < 100:  # If we got fewer tracks than requested, we're out of recommendations
                break
        
        # Create playlist
        playlist = self.sp.user_playlist_create(user=self.user_id, name=name, public=True)
        
        # Add tracks in batches of 100
        for i in range(0, len(tracks), 100):
            self.sp.user_playlist_add_tracks(self.user_id, playlist['id'], tracks[i:i+100])
            time.sleep(1)  # Rate limiting
        
        return playlist['external_urls']['spotify']  # Return playlist URL
    
    def create_mood_playlist(self, mood, name=None):
        """Create a playlist based on mood."""
        # Define mood parameters
        mood_params = {
            'happy': {'target_valence': 0.8, 'target_energy': 0.8},
            'sad': {'target_valence': 0.2, 'target_energy': 0.3},
            'energetic': {'target_valence': 0.6, 'target_energy': 0.9},
            'chill': {'target_valence': 0.5, 'target_energy': 0.3},
            'focus': {'target_valence': 0.5, 'target_energy': 0.4, 'target_instrumentalness': 0.5}
        }
        
        if mood not in mood_params:
            return None
        
        # Get seed tracks
        top_tracks = self.get_top_tracks(limit=3)
        seed_track_ids = [track['id'] for track in top_tracks]
        
        # Generate playlist name if not provided
        if name is None:
            name = f"{mood.capitalize()} Mood Playlist"
        
        # Get recommendations with mood parameters
        tracks = []
        params = mood_params[mood]
        recs = self.sp.recommendations(seed_tracks=seed_track_ids[:3], limit=50, **params)
        tracks = [track['id'] for track in recs['tracks']]
        
        # Create playlist
        playlist = self.sp.user_playlist_create(user=self.user_id, name=name, public=True)
        self.sp.user_playlist_add_tracks(self.user_id, playlist['id'], tracks)
        
        return playlist['external_urls']['spotify']  # Return playlist URL
    
    def create_bpm_playlist(self, min_bpm, max_bpm, name=None):
        """Create a playlist based on BPM (tempo) range."""
        if name is None:
            name = f"BPM {min_bpm}-{max_bpm} Playlist"
        
        # Get seed tracks
        top_tracks = self.get_top_tracks(limit=3)
        seed_track_ids = [track['id'] for track in top_tracks]
        
        # Get recommendations with BPM parameters
        tracks = []
        recs = self.sp.recommendations(
            seed_tracks=seed_track_ids[:3],
            limit=50,
            min_tempo=min_bpm,
            max_tempo=max_bpm
        )
        tracks = [track['id'] for track in recs['tracks']]
        
        # Create playlist
        playlist = self.sp.user_playlist_create(user=self.user_id, name=name, public=True)
        self.sp.user_playlist_add_tracks(self.user_id, playlist['id'], tracks)
        
        return playlist['external_urls']['spotify']  # Return playlist URL