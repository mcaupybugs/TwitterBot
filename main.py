import os
import requests
import json
import openai
import random
from requests_oauthlib import OAuth1Session

openai.api_key = ""
openai.api_base = "" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview' # this may change in the future

chatgpt_model_name='' #This will correspond to the custom name you chose for your deployment when you deployed a model. 

# Send a completion call to generate an answer
response = openai.ChatCompletion.create(
                  engine=chatgpt_model_name,
                  messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "What are the top trending keywords in tech. Please give keywords only '/' seperated and no extra text"}
                    ]
                )
keywords = response['choices'][0]['message']['content']
keywordsList = keywords.split('/')
print(keywordsList)
tweetMessageString = "Make a tweet on " + random.choice(keywordsList)
print(tweetMessageString)
tweetResponse = openai.ChatCompletion.create(
                  engine=chatgpt_model_name,
                  messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": tweetMessageString}
                    ]
                    ,max_tokens=200
                )
print(tweetResponse['choices'][0]['message']['content'])

tweet = tweetResponse['choices'][0]['message']['content']
consumer_key = ""
consumer_secret = ""

payload = {"text" : tweet}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)


# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

