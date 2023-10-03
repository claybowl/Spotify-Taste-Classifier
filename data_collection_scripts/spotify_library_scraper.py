#!/usr/bin/env python3
import os
import glob
import csv
import spotipy
import spotipy.util as util
from tqdm import tqdm


def append_dict_to_csv(filename, data_dict):
    file_exists = os.path.isfile(filename)
    fieldnames = data_dict.keys()

    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data_dict)


def get_tracks(scope, client_id, client_secret, redirect_uri, user_id):
    for file in glob.glob(".cache*"):
        os.remove(file)
    token = util.prompt_for_user_token(
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)

        track_data = []
        offset = 0
        limit = 50

        filename = f'spotify_tracks_{user_id}.csv'
        if os.path.exists(f'Data/{filename}'):
            os.remove(f'Data/{filename}')

        while True:
            results = sp.current_user_saved_tracks(limit=limit, offset=offset)
            total_tracks = results['total']
            if not results['items']:
                break

            for item in tqdm(results['items'], total=total_tracks, initial=offset, desc="Fetching tracks"):
                track = item['track']
                album = sp.album(track['album']['id'])
                audio_features = sp.audio_features([track['id']])[0]

                metadata = {
                    'user_id': user_id,
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'release_date': track['album']['release_date'],
                    'popularity': track['popularity'],
                    'duration_ms': track['duration_ms'],
                    'explicit': track['explicit'],
                    'uri': track['uri'],
                    'primary_genre': album['genres'][0] if album['genres'] else 'Unknown'
                }

                metadata.update(audio_features)
                track_data.append(metadata)

                append_dict_to_csv(f'Data/{filename}', metadata)

            offset += limit

        return track_data
    else:
        return ("Can't get token for client_id: ", client_id)


if __name__ == '__main__':
    # username = '224hap4se67crjr4hva6nz74y'
    # Aaron's client_id is 'c0f4c1d2bc644aae97e16ff177eaf908'
    # Aaron's client_secret is '91da77620f3e4aad8e1d897fe3777e6d'
    scope = 'user-library-read'
    client_id = input("What is your Spotify client_id? (stores as client_id)\n")
    client_secret = input("What is you Spotify Client_secret? (stores as client_secret)\n")
    redirect_uri = 'http://localhost:8080/'
    user_id = input("Whose music is this? (stores as user_id): ")
    tracks = get_tracks(scope, client_id, client_secret, redirect_uri, user_id)
    f"Your Spotify tracks have been saved to 'spotify_tracks_{user_id}.csv'"
