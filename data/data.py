import requests
import json
import pandas
import itertools

channel_ids = ["UCzIO0iX4yKW2P4NkmmKq1PA"]
API_KEY = "AIzaSyDIpDWDr-KkwYUMpaC1bbXBIhNn0EtAE48"

for y,channel_id in enumerate(channel_ids):
    url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}'
    response = requests.get(url)
    channel_info = response.json()
    data = pandas.DataFrame(channel_info["items"][0]["snippet"])
    data.insert(1,"id",channel_info["items"][0]["id"])
    data.insert(1,"Url","https://www.youtube.com/"+channel_info["items"][0]["snippet"]["customUrl"])
    data.drop(columns=["localized","thumbnails"],inplace=True)
    data.drop(index=["medium","high","title","description"],inplace=True)
    vidurl = f'https://www.googleapis.com/youtube/v3/search?part=id&channelId={channel_id}&maxResults=50&key={API_KEY}'
    vidresponse = requests.get(vidurl)
    print(vidresponse.json())
    video_ids = [item['id']['videoId'] for item in vidresponse.json()['items']]
    video_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={",".join(video_ids)}&key={API_KEY}'
    video_response = requests.get(video_url)
    video_info = video_response.json()
    data['Tags'] = None
    tags_list = [video['snippet'].get('tags', []) for video in video_info['items']]
    tags = list(itertools.chain(*tags_list))
    data.at["default", 'Tags'] = tags
    data['Video Titles'] = None
    vidtit_list = [video['snippet'].get('title', []) for video in video_info['items']]
    data.at["default", 'Video Titles'] = vidtit_list
    data['Video Description'] = None
    videsc_list = [video['snippet'].get('description', []) for video in video_info['items']]
    data.at["default", 'Video Description'] = videsc_list
    print(data)
    data.to_csv(f"data{y}.csv")