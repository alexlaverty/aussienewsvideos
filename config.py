import os

# List of YouTube channel feed URLs
channel_feed_urls = [
    'https://www.youtube.com/feeds/videos.xml?channel_id=UC5T7D-Dh1eDGtsAFCuwv_Sw',  # 7News
    'https://www.youtube.com/feeds/videos.xml?channel_id=UCIYLOcEUX6TbBo7HQVF2PKA',  # 9News
    'https://www.youtube.com/feeds/videos.xml?channel_id=UCoMdktPbSTixAyNGwb-UYkQ',  # SkyNews
    'https://www.youtube.com/feeds/videos.xml?channel_id=UCVgO39Bk5sMo66-6o6Spn6Q',  # ABC News (Australia)
    'https://www.youtube.com/feeds/videos.xml?channel_id=UC64A-bbH15b5kN5A32CErOA',  # 10News
    'https://www.youtube.com/feeds/videos.xml?channel_id=UCX15yQQOgUllNFd8wNRV1KQ',  # A Current Affair
]

# Reddit credentials
reddit_credentials = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT'),
    'username': os.getenv('REDDIT_USERNAME'),
    'password': os.getenv('REDDIT_PASSWORD')
}

# Subreddit name
subreddit_name = "AussieNewsVideos"

