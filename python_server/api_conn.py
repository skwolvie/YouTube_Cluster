import csv
import os
import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery

api_key= "AIzaSyB4JJHQzYe3uT8KkyVO1L1V9iNl15LINrk"

def get_youtube_credentials():
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    client_secrets_file = "sachinsm2022.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    
    return credentials

def get_subscribed_channels(youtube):
    request = youtube.subscriptions().list(
        part='snippet',
        mine=True,
        maxResults=50
    )

    channels = []
    while request is not None:
        response = request.execute()
        channels += response.get("items", [])
        request = youtube.subscriptions().list_next(request, response)

    channel_data = []
    for channel in channels:
        channel_data.append({
            "channel_title": channel["snippet"]["title"],
            "channel_descr": channel["snippet"]["description"],
            "channel_id": channel["snippet"]["resourceId"]["channelId"]
        })

    df = pd.DataFrame(channel_data)
    df.to_csv("subscribed_channels.csv", index=False)
    print("The data has been saved to subscribed_channels.csv")
    print(df.info())
    return df    

def write_video_metadata_to_csv(channel_ids, api_key):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    video_metadata = []
    for channel_id in channel_ids:
        request = youtube.search().list(
            part='id',
            type='video',
            channelId=channel_id,
            maxResults=20  # Maximum allowed results per request
        )

        response = request.execute()
        try:
            for item in response['items']:
                video_id = item['id']['videoId']
                video_details = youtube.videos().list(
                    part='snippet,topicDetails',
                    id=video_id
                ).execute()

                video = video_details['items'][0]

                tags = video['snippet'].get('tags', [])
                topics = video.get('topicDetails', {}).get('topicCategories', [])

                video_metadata.append({
                    'channel_id': channel_id,
                    'video_id': video_id,
                    'video_title': video['snippet']['title'],
                    'published_at': video['snippet']['publishedAt'],
                    'video_tags': ','.join(tags),
                    'video_topics': ','.join(topics)
                })

                # Check if there are more videos to retrieve
                request = youtube.search().list_next(request, response)
                df = pd.DataFrame(video_metadata)
                df.to_csv('youtube_video_metadata_part.csv', index=False)
        except:
              df = pd.DataFrame(video_metadata)
              df.to_csv('youtube_video_metadata.csv', index=False)

    df = pd.DataFrame(video_metadata)
    df.to_csv('youtube_video_metadata.csv', index=False)
    return df