import os
import time
import configparser
from crawler.driver_setup import driver_start
from crawler.profile_scraper import ProfileScraper
from crawler.post_scraper import PostScraper
from crawler.queue_handler import QueueHandler
from crawler.storage_handler import StorageHandler

# Load environment variables
config = configparser.ConfigParser()
config.read('config.ini')

LINKEDIN_USERNAME = config.get('LinkedIn', 'username')
LINKEDIN_PASSWORD = config.get('LinkedIn', 'password')
RAPIDAPI_KEY = config.get('LinkedIn', 'RAPIDAPI_KEY')
DRIVER_PATH = config.get('LinkedIn', 'EDGE_DRIVER_PATH', fallback='/usr/local/bin/msedgedriver')

# URL pattern for valid profile URLs
VALID_PROFILE_URL_PREFIX = "https://www.linkedin.com/in/"
TARGET_PROFILE_COUNT = 50

def is_valid_profile_url(url):
    """Check if the URL is a valid LinkedIn profile URL."""
    return url.startswith(VALID_PROFILE_URL_PREFIX) and 'overlay' not in url and '?' not in url

def main():
    # Set up the Selenium driver and other components
    driver = driver_start(DRIVER_PATH, hide_browser=False)
    profile_scraper = ProfileScraper(driver)
    post_scraper = PostScraper(RAPIDAPI_KEY)
    queue_handler = QueueHandler()
    storage_handler = StorageHandler()

    # Login to LinkedIn
    print("Logging in to LinkedIn...")
    profile_scraper.login(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)

    # Initialize with the start URL
    start_url = "https://www.linkedin.com/in/benmlang/"
    queue_handler.add_to_queue(start_url)

    # Recursive scraping
    all_profiles_data = []
    all_posts_data = []
    visited_profiles = set()

    while not queue_handler.is_queue_empty() and len(all_profiles_data) < TARGET_PROFILE_COUNT:
        # Get next profile URL from queue
        profile_url = queue_handler.get_from_queue()
        
        # Skip if this profile has already been visited
        if profile_url in visited_profiles:
            continue
        visited_profiles.add(profile_url)

        print(f"Processing profile: {profile_url}")

        # Scrape posts for the profile
        posts = post_scraper.get_posts(profile_url)
        
        if posts:
            # Collect profile data
            profile_data = {
                "profile_url": profile_url,
                "post_count": len(posts)
            }
            all_profiles_data.append(profile_data)
            all_posts_data.extend(posts)
            
            print(f"Saved {len(posts)} posts for {profile_url}")
        
        # Add valid connections of this profile to the queue
        connected_profiles = profile_scraper.scrape_profiles(profile_url)
        for connection in connected_profiles:
            if is_valid_profile_url(connection) and connection not in visited_profiles:
                queue_handler.add_to_queue(connection)

        # Optional: Delay between requests to avoid rate limits
        time.sleep(2)

    # Save all profiles and posts to JSON files
    storage_handler.save_profiles(all_profiles_data)
    storage_handler.save_posts(all_posts_data)
    
    print("Data collection complete. Profiles and posts saved to JSON files.")

    # Close the driver
    driver.quit()

main()
