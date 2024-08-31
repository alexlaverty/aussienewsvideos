# aussienewsvideos

## Overview

This script automates the process of discovering new videos, filtering them by date, and publishing the top ones to a subreddit.

<https://www.reddit.com/r/AussieNewsVideos/>

## Features

* Retrieves video details from a list of channel feed URLs
* Filters videos to include only those published today in Australian Eastern Standard Time (AEST)
* Sorts videos by views in descending order
* Publishes the top 10 most viewed videos to a specified subreddit
* Writes video data to a CSV file for record-keeping

## Usage
* Configuration: Set up your configuration in config.py:
  * `channel_feed_urls`: List of channel feed URLs
  * `reddit_credentials`: Dictionary containing Reddit API credentials
  * `subreddit_name`: Name of the subreddit to publish to
* Running the script: Execute the script using `python main.py`
* Output: The script will publish the top 10 most viewed videos to the specified subreddit and write video data to videos.csv

## Requirements
* Python 3.x
* requests
* beautifulsoup4
* pytz
* praw
* csv

## Note

Make sure to replace the reddit_credentials dictionary with your own Reddit API credentials.
Adjust the channel_feed_urls list to include the desired channel feed URLs.
Modify the subreddit_name variable to specify the subreddit to publish to.
