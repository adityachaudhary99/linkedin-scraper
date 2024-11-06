from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import os

def driver_start(DRIVER_PATH, hide_browser=False):
    DRIVER_PATH = 'C:\\Users\\adity\\Downloads\\edgedriver_win64\\msedgedriver.exe'
    edge_options = Options()
 
    if hide_browser:
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--disable-popup-blocking")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.maximize_window()
    return driver
