from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
import os
import time
import requests
from urllib.request import urlretrieve

chromedriver_path = "C:/Users/Dell/Documents/Projects/Scrapper/chromedriver.exe" #path for chromedriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
url = "https://www.google.com/search?q=Mercedez+benz&tbm=isch"
driver.get(url)

# Scroll all the way down to load all images
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('img', {'class': 'rg_i Q4LuWd'})
len_containers = len(containers)
print(f"Found {len_containers} image containers")

# Create a directory to save the images
dir_name = "Mercedez_benz_images"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# Download the images
image_count = 0
for container in containers:
    if image_count >= 100:  # Adjust the limit as needed
        break
    img_src = container['src']
    try:
        img_name = f"{dir_name}/Mercedez_benz_{image_count}.jpg"
        urlretrieve(img_src, img_name)
        image_count += 1
        print(f"Downloaded image {image_count}")
    except Exception as e:
        print(f"Error downloading image: {e}")

driver.quit()
print("Images downloaded successfully!")
