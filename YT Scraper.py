import openpyxl
import time
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
print(pd.__version__)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.youtube.com/@JollyOlive/videos")


# ...
WAIT_IN_SECONDS = 2
last_height = driver.execute_script(
    "return document.documentElement.scrollHeight")

while True:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
    # Wait for new videos to show up
    time.sleep(WAIT_IN_SECONDS)

    # Calculate the new document height and compare it with the last height
    new_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


channel_title = driver.find_element(
    By.XPATH, '//yt-formatted-string[contains(@class, "ytd-channel-name")]').text
handle = driver.find_element(
    By.XPATH, '//yt-formatted-string[@id="channel-handle"]').text
subscriber_count = driver.find_element(
    By.XPATH, '//yt-formatted-string[@id="subscriber-count"]').text
titles = driver.find_elements(By.ID, "video-title")
views = driver.find_elements(By.XPATH, '//div[@id="metadata-line"]/span[1]')
video_age = driver.find_elements(
    By.XPATH, '//div[@id="metadata-line"]/span[2]')
thumbnails = driver.find_elements(
    By.XPATH, '//a[@id="thumbnail"]/yt-image/img')

videos = []
for title, view, video_age, thumb in zip(titles, views, video_age, thumbnails):
    video_dict = {
        'title': title.text,
        'views': view.text,
        'video age': video_age.text,
        'thumbnail': thumb.get_attribute('src')
    }
    videos.append(video_dict)

df = pd.DataFrame(videos)
df.to_excel('jolly.xlsx')
pprint(videos)
