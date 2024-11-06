# LinkedIn Web Scraper and Data Analysis

## Project Overview
This project is a LinkedIn web scraper designed to gather LinkedIn posts from user profiles, analyzing trends and patterns in the collected data. The scraper is implemented with Selenium and Edge WebDriver, and the data analysis is done in a Jupyter Notebook. Docker is used to streamline deployment and execution, while Poetry handles dependency management.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Poetry](https://python-poetry.org/docs/#installation)
- LinkedIn account access (manual login may be required due to LinkedIn's access restrictions)

## Project Structure

linkedin-crawler/
├── crawler/
│   ├── __init__.py
│   ├── crawler.py               # Main crawler logic
│   ├── driver_setup.py          # initialize the driver
│   ├── config.ini               # Configuration file
│   ├── post_scraper.py          # get post data using api
│   ├── profile_scraper.py       # Scraping profiles and push to queue
│   └── storage_handler.py       # save post and profile data as json
├── data/
│   ├── posts.json, posts_new.json           # Scraped posts data
│   └── profiles.json, profiles_new.json     # Scraped profile data
├── analysis/
│   └── analysis.ipynb           # Jupyter Notebook for analysis
├── Dockerfile                   # Docker setup for the project
├── docker-compose.yaml          # Docker compose file for redis setup
├── README.md                    # Detailed setup and usage instructions
├── poetry.lock                  # Poetry lockfile
└── pyproject.toml               # Poetry dependencies and project configuration

---

## Setup Instructions

### Step 1: Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/adityachaudhary99/linkedin-scraper.git
cd linkedin-scraper
```

### Step 2: Install Dependencies with Poetry
Run the following command to install the dependencies:

```bash
poetry install
```

### Step 3: Configure config.ini
Edit the config.ini file to set the necessary configurations:

LinkedIn_Credentials: LinkedIn username and password
edgedriver_path: Path to the Edge WebDriver (Docker handles this path)
RapidAPI-key


### Running the Crawler
#### Using Docker
Build and run the Docker container as follows:

Build the Docker image:

```bash
docker build -t linkedin-crawler .
```

Run the container:

```bash
docker run linkedin-crawler
```

This will initiate the crawler, scrape profiles and posts, and store them in data/posts_new.json and data/profiles_new.json.



### Running Locally
If you prefer to run locally (requires Edge WebDriver installed locally):

Install the necessary dependencies with Poetry:

```bash
poetry install
```

Run the crawler:

```bash
poetry run python crawler.py
```


### Running the Jupyter Notebook
Ensure that Jupyter is installed:

```bash
poetry add jupyter
```

Start Jupyter Notebook:

```bash
jupyter notebook analysis/analysis.ipynb
```

This will open the notebook where you can run cells for data analysis.


## Crawler Design
The scraper uses an Object-Oriented structure for flexibility and modularity. Key components include:

crawler.py: The entry point, initializes the scraping process and manages the queue of profiles.
profile_scraper.py: Manages interactions with LinkedIn using Selenium and Edge WebDriver.
post_scraper.py: Gets post data for user profiles using Rapid API.
storage_handler.py: Responsible for saving scraped data to JSON files.
queue_handler.py: Responsible for handling profile URL queues.

The crawler uses a queue to handle profile URLs, managing depth-first traversal to reach the specified limit of profiles.