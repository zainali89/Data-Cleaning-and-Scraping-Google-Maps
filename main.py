from doctest import master
import threading
from tkinter import E
from time import sleep
from GMB.search_result_page import SearchResult
import GMB.constants as const
import numpy as np
import os
import pandas as pd
#from numba import jit, cuda
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time



try:
    def scrapeData(category,Location):
        bot = SearchResult(tearDown=False,prof=category,loc=Location)
        bot.land_on_page()
        bot.search(category,Location)
        bot.pull_search_results()
        #bot.pull_listings_data()
        bot.quit_browser()
except Exception as e:
    raise

#running this function to get categories form csv file


#scrapeData(const.To_SEARCH_CATEGORIES[0])
#@jit
def start_scraping_by_list(CategoryList, Location):
    for Category in CategoryList:
        for Loc in Location:
            file = Category + "_" + Loc + '.csv'
            #if not (os.path.isfile(f'{const.DIRECTORY_NAME}/{file}')):
            scrapeData(str(Category).strip(),str(Loc).strip())
            #else:
             #   print(file, " already scraped")

splits = np.array_split(const.CATEGORIES_LIST, const.NUMBER_OF_THREADS)
print(const.CATEGORIES_LIST)

for category_list in splits:
    Thread = threading.Thread(target=start_scraping_by_list, args=(category_list,const.LOCATION_LIST))
    Thread.start()
    

