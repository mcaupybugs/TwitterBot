import os
import requests
import json
import openai
import random
from requests_oauthlib import OAuth1Session

openai.api_key = os.environ.get("OPENAPI_KEY")
openai.api_base = os.environ.get("OPENAPI_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview' # this may change in the future

chatgpt_model_name=os.environ.get("MODEL_NAME") #This will correspond to the custom name you chose for your deployment when you deployed a model. 

def callGPT():
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
    
    return tweetResponse['choices'][0]['message']['content']

