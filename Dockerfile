# Use a lightweight Python image as the base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install necessary packages for Edge and ChromeDriver
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg \
    # Install dependencies for Selenium
    wget \
    unzip \
    # Install Edge and EdgeDriver
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg \
    && sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list' \
    && apt-get update && \
    apt-get install -y microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

# Download and install EdgeDriver matching the Edge version
RUN EDGEDRIVER_VERSION=$(microsoft-edge --version | sed -E 's/^Microsoft Edge ([0-9]+).*/\1/') && \
    curl -o /tmp/edgedriver.zip https://msedgedriver.azureedge.net/$EDGEDRIVER_VERSION/edgedriver_linux64.zip && \
    unzip /tmp/edgedriver.zip -d /usr/local/bin/ && \
    rm /tmp/edgedriver.zip

# Install poetry and project dependencies
RUN pip install poetry && \
    poetry install && \
    poetry add redis configparser selenium lxml beautifulsoup4 python-dotenv requests

# Define entrypoint command to run the crawler
CMD ["poetry", "run", "python", "crawler.py"]
