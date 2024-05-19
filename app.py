import requests
import csv
from datetime import datetime, timedelta
import pytz
import praw
from config import channel_feed_urls, reddit_credentials, subreddit_name
from bs4 import BeautifulSoup

def get_latest_videos_from_feed(channel_feed_urls):
    video_details = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for url in channel_feed_urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        entries = soup.find_all('entry')

        for entry in entries:  # Get all videos
            video_title = entry.find('title').text
            video_url = entry.find('link', {'rel': 'alternate'})['href']
            published_date = entry.find('published').text
            views = entry.find('media:statistics')['views'] if entry.find('media:statistics') else '0'
            views = int(views)
            channel_name = entry.find('author').find('name').text
            video_details.append((video_title, video_url, published_date, views, channel_name))

    return video_details

def filter_videos_by_date(videos):
    aest_tz = pytz.timezone('Australia/Sydney')
    today_aest = datetime.utcnow().astimezone(aest_tz).date()
    today_str_aest = today_aest.isoformat()

    filtered_videos = []
    for video in videos:
        title = video[0]
        published = video[2]
        published_datetime = datetime.strptime(published, '%Y-%m-%dT%H:%M:%S%z')
        converted_published = published_datetime.astimezone(aest_tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        #print(f"Title: {title}\nPublished: {published}\nConverted Publish Date: {converted_published}\ntoday_str_aest: {today_str_aest}")
        if converted_published.startswith(today_str_aest):
            #print(f"ACCEPTED: {converted_published} - {title}")
            filtered_videos.append(video)
        # else:
        #     print(f"REJECTED: {converted_published} - {title}")

    return filtered_videos

def write_to_csv(video_data):
    # Function to write video data to a CSV file
    with open('videos.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'URL', 'Published', 'Views', 'Channel Name'])
        writer.writerows(video_data)

def check_duplicate_url(url):
    # Function to check if the URL has already been posted
    try:
        with open('videos.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if row[1] == url:
                    return True
    except FileNotFoundError:
        pass
    return False

def publish_to_subreddit(reddit, subreddit_name, video_data):
    # Function to publish video data to a subreddit
    subreddit = reddit.subreddit(subreddit_name)
    published_videos = []  # List to store published video data
    for title, url, published, views, channel_name in video_data:
        if not check_duplicate_url(url):
            try:
                submission = subreddit.submit(title=title, url=url)
                print(f"Published: {title}")
                published_videos.append((title, url, published, views, channel_name))
            except Exception as e:
                print(f"Failed to publish {title}: {e}")
        else:
            print(f"URL already published: {url}")
            #published_videos.append((title, url, published, views, channel_name, False))

    # Write published videos to CSV file
    if published_videos:
        with open('videos.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for video in published_videos:
                writer.writerow(video)

def main():
    # Get the latest videos
    all_videos = get_latest_videos_from_feed(channel_feed_urls)

    # Filter videos to include only those published today in AEST
    todays_videos = filter_videos_by_date(all_videos)

    # Sort videos by views in descending order
    sorted_videos = sorted(todays_videos, key=lambda x: x[3], reverse=True)

    # Get the top 10 most viewed videos
    top_videos = sorted_videos[:10]

    # Write the top videos to a CSV file
    #write_to_csv(top_videos)

    # Authenticate with Reddit
    reddit = praw.Reddit(client_id=reddit_credentials['client_id'],
                         client_secret=reddit_credentials['client_secret'],
                         user_agent=reddit_credentials['user_agent'],
                         username=reddit_credentials['username'],
                         password=reddit_credentials['password'])

    # Publish the top videos to the specified subreddit
    publish_to_subreddit(reddit, subreddit_name, top_videos)

if __name__ == "__main__":
    main()
