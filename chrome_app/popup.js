async function getYouTubeCredentials() {
  const clientId = "yourClientId.apps.googleusercontent.com";
  const scopes = ["https://www.googleapis.com/auth/youtube.readonly"];

  return await gapi.auth2.init({ clientId, scope: scopes.join(" ") });
}

async function getSubscribedChannels(youtube) {
  const request = youtube.subscriptions.list({
    part: "snippet",
    mine: true,
    maxResults: 50,
  });

  const response = await request.execute();

  const channels = response.items;

  const channelData = [];
  channels.forEach((channel) => {
    channelData.push({
      channelTitle: channel.snippet.title,
      channelDescr: channel.snippet.description,
      channelId: channel.snippet.resourceId.channelId,
    });
  });

  return channelData;
}

async function writeVideoMetadataToCSV(channelIds, apiKey) {
  const youtube = gapi.client.youtube({
    version: "v3",
    apiKey,
  });

  const videoMetadata = [];
  for (const channelId of channelIds) {
    const request = youtube.search.list({
      part: "id",
      type: "video",
      channelId,
      maxResults: 20,
    });

    const response = await request.execute();

    for (const item of response.items) {
      const videoId = item.id.videoId;
      const videoDetails = await youtube.videos.list({
        part: "snippet,topicDetails",
        id: videoId,
      });

      const video = videoDetails.items[0];

      const tags = video.snippet.tags || [];
      const topics = video.topicDetails ? video.topicDetails.topicCategories : [];

      videoMetadata.push({
        channelId,
        videoId,
        videoTitle: video.snippet.title,
        publishedAt: video.snippet.publishedAt,
        videoTags: tags.join(","),
        videoTopics: topics.join(","),
      });
    }
  }

  return videoMetadata;
}
