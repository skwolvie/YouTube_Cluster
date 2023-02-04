# -*- coding: utf-8 -*-

import os
import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "../secrets/sks1999_desktop.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

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
    df.to_csv("../data/subscribed_channels.csv", index=False)
    print("The data has been saved to subscribed_channels.csv")



if __name__ == "__main__":
    main()
