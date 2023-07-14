import twitter_service
import redis
import os
import gpt_service
import json

twitter = twitter_service.make_token()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
token_url = "https://api.twitter.com/2/oauth2/token"

t = twitter_service.r.get("token")
bb_t = t.decode("utf8").replace("'", '"')
data = json.loads(bb_t)

refreshed_token = twitter.refresh_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    refresh_token=data["refresh_token"],
)

st_refreshed_token = '"{}"'.format(refreshed_token)
j_refreshed_token = json.loads(st_refreshed_token)
twitter_service.r.set("token", j_refreshed_token)

tweet = gpt_service.callGPT()
payload = {"text": "{}".format(tweet)}
twitter_service.post_tweet(payload, refreshed_token)