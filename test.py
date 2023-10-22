from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('/Users/zainali/scraping1/chromedriver')
driver.implicitly_wait(15)
driver.get("https://www.youtube.com/channel/UCgyMIMxCZhZIZz6UzldPPFg/videos")
all_videos = driver.find_elements(By.TAG_NAME,'ytd-grid-video-renderer')
print('Before loop')
for video in all_videos:
    print('Within loop')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    all_videos = driver.find_elements(By.TAG_NAME,'ytd-grid-video-renderer')
    title = video.find_element_by_id('video-title').get_attribute('innerHTML')
    print(title)