from doctest import master
import imp
import threading
from tkinter import E
from time import sleep
import sys
from listing_page import ReviewsResult
import numpy as np
import os
import pandas as pd
from numba import jit, cuda
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

os.chdir('/Users/zainali/scraping1/GMB listings 1/files')
NUMBER_OF_THREADS = 1
categories_list_file = []

for file in os.listdir(os.getcwd()):
    if file.endswith('.csv'):
        if not file.__contains__('URL') and not file.__contains__('All in One Data') and not file.__contains__('Meta Data') and not 'review' in file:
            categories_list_file.append(file)
print(categories_list_file)

os.chdir('/Users/zainali/scraping1/GMB listings 1/Scrape Reviews')

try:
    def scrapeReviews(file):
        bot = ReviewsResult(tearDown=False,File_name=file)
        bot.land_on_default_page()
        bot.pull_reviews_results()
        #bot.pull_listings_data()
        bot.quit_browser()
except Exception as e:
    raise

#running this function to get categories form csv file


#scrapeData(const.To_SEARCH_CATEGORIES[0])
#@jit
def start_scraping_by_list(file_list, Location):
    for file in file_list:
        scrapeReviews(file)

splits = np.array_split(categories_list_file, NUMBER_OF_THREADS)
print(splits)

for file_list in splits:
    Thread = threading.Thread(target=start_scraping_by_list, args=(file_list,''))
    Thread.start()
    

