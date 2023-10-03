#!/usr/bin/env python3
import os
import spotipy
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import spotipy.util as util

# Set your credentials here
os.environ["SPOTIPY_CLIENT_ID"] = "052ac62e09364e79837503959c9ee117"
os.environ["SPOTIPY_CLIENT_SECRET"] = "6ab119c595c94646bba0adc9515574a8"

# Set the playlist ID here
playlist_id = "5pjnr70zFIUAXc72YJie8U"

# Initialize Spotipy with the client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Function to get all tracks in a playlist


def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


# Get all tracks in the playlist
playlist_tracks = get_playlist_tracks(sp, playlist_id)

with open('playlist_tracks.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['name', 'artist', 'album', 'spotify_id',
                  'duration_ms', 'explicit', 'uri', 'primary_genre', 'danceability', 'energy', 'key',
                  'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                  'liveness', 'valence', 'tempo', 'time_signature']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for track in playlist_tracks:
        t = track['track']
        album = sp.album(t['album']['id'])
        audio_features = sp.audio_features([t['id']])[0]

        writer.writerow({
            'name': t['name'],
            'artist': t['artists'][0]['name'],
            'album': t['album']['name'],
            'spotify_id': t['id'],
            'duration_ms': t['duration_ms'],
            'explicit': t['explicit'],
            'uri': t['uri'],
            'primary_genre': album['genres'][0] if album['genres'] else 'Unknown',
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'key': audio_features['key'],
            'loudness': audio_features['loudness'],
            'mode': audio_features['mode'],
            'speechiness': audio_features['speechiness'],
            'acousticness': audio_features['acousticness'],
            'instrumentalness': audio_features['instrumentalness'],
            'liveness': audio_features['liveness'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo'],
            'time_signature': audio_features['time_signature']
        })

print("Tracks and metadata have been saved to 'playlist_tracks.csv'.")