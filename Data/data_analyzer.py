import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('Data/spotify_tracks_clayton.csv')

# Convert release_date column to a datetime object
df['release_date'] = pd.to_datetime(df['release_date'])

# Calculate average values of audio features
average_audio_features = df[['danceability', 'energy', 'valence']].mean()

# Analyze the distribution of popularity scores
popularity_distribution = df['popularity'].hist(bins=20)
plt.xlabel('Popularity')
plt.ylabel('Frequency')
plt.title('Distribution of Track Popularity')
plt.show()

# Analyze the most common genres
top_genres = df['primary_genre'].value_counts().head(10)
top_genres.plot(kind='bar')
plt.xlabel('Genre')
plt.ylabel('Frequency')
plt.title('Top 10 Genres')
plt.show()

# More analysis and visualizations...
