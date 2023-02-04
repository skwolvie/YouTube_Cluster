const apiKey = 'AIzaSyBxNjBty9xn07ZBxbXpYYSs9oeWecpvmmY';
const channelId = 'UCsycZrTpSQwkEPUI4qkeEig';

const url = `https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId=${channelId}&key=${apiKey}`;

fetch(url)
  .then(response => response.json())
  .then(data => {
    const subscriptions = data.items;
    subscriptions.forEach(subscription => {
      console.log(subscription.snippet.title);
    });
  })
  .catch(error => console.error(error));
