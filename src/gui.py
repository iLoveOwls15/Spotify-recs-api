import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

class SpotifyApp:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        
        # Configure the root window
        self.root.title("Spotify Playlist Generator")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(self.main_frame, text="Spotify Playlist Generator", font=("Helvetica", 16)).pack(pady=10)
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Recommendations tab
        self.rec_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.rec_tab, text="Recommendations")
        self.setup_recommendations_tab()
        
        # Mood tab
        self.mood_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.mood_tab, text="Moods")
        self.setup_mood_tab()
        
        # BPM tab
        self.bpm_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.bpm_tab, text="BPM")
        self.setup_bpm_tab()
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10,0))
    
    def setup_recommendations_tab(self):
        # Create frame with padding
        frame = ttk.Frame(self.rec_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Time range selection
        ttk.Label(frame, text="Time Range:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.time_range = tk.StringVar(value="medium_term")
        time_range_combo = ttk.Combobox(frame, textvariable=self.time_range)
        time_range_combo['values'] = ('short_term', 'medium_term', 'long_term')
        time_range_combo['state'] = 'readonly'
        time_range_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(frame, text="(last 4 weeks, 6 months, or all time)").grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # Number of tracks
        ttk.Label(frame, text="Number of Tracks:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.num_tracks = tk.IntVar(value=100)
        track_options = [50, 100, 200, 500, 1000, 5000, 9999]
        track_spin = ttk.Combobox(frame, textvariable=self.num_tracks, width=5)
        track_spin['values'] = track_options
        track_spin.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Playlist name
        ttk.Label(frame, text="Playlist Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.playlist_name = tk.StringVar(value="My Recommendations")
        ttk.Entry(frame, textvariable=self.playlist_name, width=30).grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Create button
        ttk.Button(frame, text="Create Playlist", command=self.create_recommendations).grid(row=3, column=0, columnspan=3, pady=20)
    
    def setup_mood_tab(self):
        # Create frame with padding
        frame = ttk.Frame(self.mood_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Mood selection
        ttk.Label(frame, text="Select Mood:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mood = tk.StringVar(value="happy")
        mood_combo = ttk.Combobox(frame, textvariable=self.mood, width=15)
        mood_combo['values'] = ('happy', 'sad', 'energetic', 'chill', 'focus')
        mood_combo['state'] = 'readonly'
        mood_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Playlist name
        ttk.Label(frame, text="Playlist Name (optional):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.mood_playlist_name = tk.StringVar()
        ttk.Entry(frame, textvariable=self.mood_playlist_name, width=30).grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Create button
        ttk.Button(frame, text="Create Mood Playlist", command=self.create_mood_playlist).grid(row=2, column=0, columnspan=3, pady=20)
    
    def setup_bpm_tab(self):
        # Create frame with padding
        frame = ttk.Frame(self.bpm_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # BPM range
        ttk.Label(frame, text="BPM Range:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        bpm_frame = ttk.Frame(frame)
        bpm_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        self.min_bpm = tk.IntVar(value=90)
        min_spin = ttk.Spinbox(bpm_frame, from_=60, to=200, textvariable=self.min_bpm, width=5)
        min_spin.pack(side=tk.LEFT)
        
        ttk.Label(bpm_frame, text=" to ").pack(side=tk.LEFT)
        
        self.max_bpm = tk.IntVar(value=120)
        max_spin = ttk.Spinbox(bpm_frame, from_=60, to=200, textvariable=self.max_bpm, width=5)
        max_spin.pack(side=tk.LEFT)
        
        # Playlist name
        ttk.Label(frame, text="Playlist Name (optional):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bpm_playlist_name = tk.StringVar()
        ttk.Entry(frame, textvariable=self.bpm_playlist_name, width=30).grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Create button
        ttk.Button(frame, text="Create BPM Playlist", command=self.create_bpm_playlist).grid(row=2, column=0, columnspan=3, pady=20)
    
    def create_recommendations(self):
        try:
            self.status_var.set("Creating playlist...")
            self.root.update_idletasks()
            
            max_tracks = self.num_tracks.get()
            time_range = self.time_range.get()
            name = self.playlist_name.get()
            
            playlist_url = self.client.create_recommendations_playlist(name=name, max_tracks=max_tracks)
            
            self.status_var.set(f"Playlist created: {name}")
            messagebox.showinfo("Success", f"Playlist '{name}' created successfully!")
            webbrowser.open(playlist_url)
        except Exception as e:
            self.status_var.set("Error creating playlist")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def create_mood_playlist(self):
        try:
            mood = self.mood.get()
            name = self.mood_playlist_name.get() or None
            
            self.status_var.set(f"Creating {mood} mood playlist...")
            self.root.update_idletasks()
            
            playlist_url = self.client.create_mood_playlist(mood, name)
            
            display_name = name if name else f"{mood.capitalize()} Mood Playlist"
            self.status_var.set(f"Playlist created: {display_name}")
            messagebox.showinfo("Success", f"Playlist '{display_name}' created successfully!")
            webbrowser.open(playlist_url)
        except Exception as e:
            self.status_var.set("Error creating playlist")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def create_bpm_playlist(self):
        try:
            min_bpm = self.min_bpm.get()
            max_bpm = self.max_bpm.get()
            name = self.bpm_playlist_name.get() or None
            
            if min_bpm >= max_bpm:
                messagebox.showerror("Error", "Minimum BPM must be less than maximum BPM")
                return
            
            self.status_var.set(f"Creating BPM {min_bpm}-{max_bpm} playlist...")
            self.root.update_idletasks()
            
            playlist_url = self.client.create_bpm_playlist(min_bpm, max_bpm, name)
            
            display_name = name if name else f"BPM {min_bpm}-{max_bpm} Playlist"
            self.status_var.set(f"Playlist created: {display_name}")
            messagebox.showinfo("Success", f"Playlist '{display_name}' created successfully!")
            webbrowser.open(playlist_url)
        except Exception as e:
            self.status_var.set("Error creating playlist")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")