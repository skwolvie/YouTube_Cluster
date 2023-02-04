import csv
import os
from googleapiclient.discovery import build

# Replace with your own API key
api_key = "YOUR_API_KEY"

# List of YouTube channel IDs
channel_ids = ["channel_id_1", "channel_id_2", "channel_id_3"]

# Define the columns for the csv file
fields = ['channel_id', 'video_id', 'title', 'published_at']

# Create the csv file
filename = "youtube_video_metadata.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
    csvwriter.writeheader()

    # Initialize the YouTube Data API v3 client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Loop through each channel ID
    for channel_id in channel_ids:
        request = youtube.search().list(
            part='id',
            type='video',
            channelId=channel_id,
            maxResults=50  # Maximum allowed results per request
        )

        while request is not None:
            # Get the next batch of videos
            response = request.execute()

            # Loop through each video
            for item in response['items']:
                video_id = item['id']['videoId']

                # Get the video details
                video_details = youtube.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()

                video = video_details['items'][0]

                # Write the video metadata to the csv file
                csvwriter.writerow({
                    'channel_id': channel_id,
                    'video_id': video_id,
                    'title': video['snippet']['title'],
                    'published_at': video['snippet']['publishedAt']
                })

            # Check if there are more videos to retrieve
            request = youtube.search().list_next(request, response)
