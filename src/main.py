import os
import time
import sys
from dotenv import load_dotenv
import tkinter as tk
import traceback

def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Debug prints
        print("Starting application...")
        print(f"CLIENT_ID: {os.getenv('CLIENT_ID')}")
        print(f"CLIENT_SECRET: {os.getenv('CLIENT_SECRET')}")
        print(f"REDIRECT_URL: {os.getenv('REDIRECT_URL')}")
        
        # Import modules after environment variables are loaded
        from client import SpotifyClient
        from gui import SpotifyApp
        
        print("Creating Spotify client...")
        # Initialize Spotify client
        client = SpotifyClient(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_URL")
        )
        print("Spotify client created successfully!")
        
        # Test the client to make sure authentication worked
        print("Testing Spotify API connection...")
        user_id = client.user_id
        print(f"Connected as user: {user_id}")
        
        # Start GUI
        print("Starting GUI...")
        root = tk.Tk()
        app = SpotifyApp(root, client)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")  # Keep console open to see error

if __name__ == "__main__":
    main()