"""
This file contains a function to “post” a tweet using X's HTTP API.

For demonstration purposes, the function simply prints the tweet
content. In a real application, you would integrate with X's API
using the requests module.
"""

import requests


def post_tweet(article):
    # Create tweet content based on the article title.
    tweet_content = f"New Article Published: {article.title}"
    # Here, you would normally send an HTTP POST request to X's API.
    # Example (commented out):
    # response = requests.post(
    #     'https://api.twitter.com/2/tweets',
    #     headers=headers,
    #     json={'text': tweet_content}
    # )
    # For demonstration, print the tweet content.
    print(f"Tweet posted: {tweet_content}")
