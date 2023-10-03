#!/usr/bin/env python3
"""Takes in youtube URL and returns .csv file
containing spotify_id, name, artist, album, and duration_ms"""
import os
import pandas as pd
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set up YouTube API credentials
YOUTUBE_API_KEY = 'AIzaSyC14MtGZ0gkjbYD3rL5cSJXDBKHAXZZ7sI'

# Set up Spotify API credentials
SPOTIFY_CLIENT_ID = '052ac62e09364e79837503959c9ee117'
SPOTIFY_CLIENT_SECRET = '6ab119c595c94646bba0adc9515574a8'

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Get Spotify API access token
def get_spotify_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(auth_url, data=auth_data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Failed to get Spotify access token')


# Initialize Spotify access token
spotify_access_token = get_spotify_access_token(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)


def convert_song(youtube_link):
    # Extract YouTube video ID from the link
    youtube_video_id = youtube_link.split('watch?v=')[-1]

    # Get video details from YouTube API
    video_response = youtube.videos().list(
        part='snippet',
        id=youtube_video_id
    ).execute()

    # Extract video title and artist
    video_title = video_response['items'][0]['snippet']['title']

    # Search for the song on Spotify
    search_url = 'https://api.spotify.com/v1/search'
    search_headers = {
        'Authorization': f'Bearer {spotify_access_token}'
    }
    search_params = {
        'q': video_title,
        'type': 'track',
        'limit': 1
    }
    search_response = requests.get(
        search_url, headers=search_headers, params=search_params)
    search_data = search_response.json()

    # Get the Spotify track ID
    spotify_track_id = search_data['tracks']['items'][0]['id']

    return {
        'youtube_video_id': youtube_video_id,
        'spotify_track_id': spotify_track_id,
        'song_title': video_title
    }


# Main function (might need to be separate file?)

def main():
    # Input YouTube URL
    youtube_url = input(
        "Enter the YouTube URL: ")

    try:
        # Convert the song and print the result
        song_data = convert_song(youtube_url)
        print(f"Song data: {song_data}")

        # Create a DataFrame and save it to a CSV
        song_df = pd.DataFrame([song_data])
        song_df.to_csv('yt_to_spotify.csv', index=False)
        print("Song data saved to 'yt_to_spotify.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
