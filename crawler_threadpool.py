import os
import time
import threading
import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed
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
DRIVER_PATH = config.get('LinkedIn', 'EDGE_DRIVER_PATH')

# URL pattern for valid profile URLs
VALID_PROFILE_URL_PREFIX = "https://www.linkedin.com/in/"
TARGET_PROFILE_COUNT = 5

def is_valid_profile_url(url):
    """Check if the URL is a valid LinkedIn profile URL."""
    return url.startswith(VALID_PROFILE_URL_PREFIX) and 'overlay' not in url and '?' not in url

def scrape_profile(profile_url, profile_scraper, post_scraper, queue_handler, visited_profiles, lock, all_profiles_data, all_posts_data):
    """Scrape data from a single LinkedIn profile and process connections."""
    with lock:
        if profile_url in visited_profiles:
            return
        visited_profiles.add(profile_url)

    print(f"Processing profile: {profile_url}")
    posts = post_scraper.get_posts(profile_url)
    
    if posts:
        profile_data = {
            "profile_url": profile_url,
            "post_count": len(posts)
        }
        with lock:
            all_profiles_data.append(profile_data)
            all_posts_data.extend(posts)
        
        print(f"Saved {len(posts)} posts for {profile_url}")

    # Add valid connections of this profile to the queue
    connected_profiles = profile_scraper.scrape_profiles(profile_url)
    with lock:
        for connection in connected_profiles:
            if is_valid_profile_url(connection) and connection not in visited_profiles:
                queue_handler.add_to_queue(connection)

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
    
    start_url = "https://www.linkedin.com/in/yrebryk/"
    queue_handler.add_to_queue(start_url)

    all_profiles_data = []
    all_posts_data = []
    visited_profiles = set()
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=2) as executor:
        while len(all_profiles_data) < TARGET_PROFILE_COUNT:
            # Fetch profiles from the queue
            profile_futures = []
            while not queue_handler.is_queue_empty() and len(profile_futures) < 5:
                profile_url = queue_handler.get_from_queue()
                # Submit profile scraping task to the executor
                profile_futures.append(
                    executor.submit(scrape_profile, profile_url, profile_scraper, post_scraper,
                                    queue_handler, visited_profiles, lock, all_profiles_data, all_posts_data)
                )

            # Wait for tasks to complete
            for future in as_completed(profile_futures):
                future.result()  # Retrieve result to handle exceptions

    # Save all profiles and posts to JSON files
    storage_handler.save_profiles(all_profiles_data)
    storage_handler.save_posts(all_posts_data)
    
    print("Data collection complete. Profiles and posts saved to JSON files.")
    driver.quit()

if __name__ == "__main__":
    main()
