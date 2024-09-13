import instaloader
import csv
import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime

def fetch(url,csv_filename):
    print("Fetching tweets from Twitter")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--window-size=1920x1080")  

    service = Service(executable_path=CM().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)  

    driver.get(url)
    time.sleep(5)
    
    for i in range(1):
        driver.execute_script("window.scrollBy(0,2000)")
        time.sleep(2)

    tweets_data = []
    tweet_elements = driver.find_elements(By.XPATH, '//article')

    max_tweets = 5
    tweet_count = 0

    for tweet in tweet_elements:
        if tweet_count >= max_tweets:
            break
        try:
            # Extract tweet text
            tweet_text = tweet.find_element(By.XPATH, './/div[@lang]').text

            # Extract tweet URL
            tweet_url = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute('href')

            # Extract tweet time
            tweet_time_iso = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
            tweet_time = datetime.strptime(tweet_time_iso, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")

            # to find image links
            images = tweet.find_elements(By.XPATH, './/img')

            if len(images) >= 2:
                img_link = images[1].get_attribute('src')  # Get the second image link
            else:
                img_link = 'No image found'

            # Store tweet data
            tweets_data.append({'news': tweet_text, 'media_link': img_link, 'timespan': tweet_time, 'for twitter video': tweet_url})
            tweet_count += 1
        except Exception as e:
            print(f"Error extracting tweet: {e}")

    # Save to a CSV file with specified column names
    df = pd.DataFrame(tweets_data)
    df.to_csv(csv_filename, index=False, columns=['news', 'media_link', 'timespan', 'for twitter video'])

    driver.quit()

# Code for Instagram scraping
L = instaloader.Instaloader()

def get_posts_data(profile, count):
    posts_data = []
    for i, post in enumerate(profile.get_posts()):
        if i >= count:
            break
        
        if post.is_video:
            media_url = post.video_url
        else:
            media_url = post.url
        
        post_info = {
            "news": post.caption,
            "media_url": media_url,  
            "timestamp": post.date_utc.strftime("%Y-%m-%d %H:%M:%S")
        }
        posts_data.append(post_info)
    return posts_data

def save_data_to_csv(posts_data, csv_filename):
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['news', 'media_url', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for post in posts_data:
            writer.writerow(post)

    print(f"Data appended to {csv_filename}")

def scrape_instagram_data(usernames, count, csv_filename):
    for username in usernames:
        print(f"Fetching data for profile: {username}")
        
        profile = instaloader.Profile.from_username(L.context, username)

        posts_data = get_posts_data(profile, count)
        print(f"Fetched {len(posts_data)} posts for {username}")

        save_data_to_csv(posts_data, csv_filename)

        time.sleep(2)



