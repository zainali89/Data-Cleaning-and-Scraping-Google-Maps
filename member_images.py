#This file has class and functions to pull data from listing page
from cmath import log
from tkinter.messagebox import ABORTRETRYIGNORE
from unicodedata import name
import pandas as pd
from lib2to3.pgen2 import driver
import GMB.constants as const
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep
from geopy.geocoders import Nominatim
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

class Images():
    def __init__(self, driver:WebDriver ,user_id):
        self.driver = driver
        self.user_id = user_id
        self.images_needed = 12



    def pull_images(self):

        #getting all gallary images
        gallary_images = ""
        try:
            gallary_div_a_tags = self.driver.find_element_by_css_selector(
                'div[data-attrid="kc:/location/location:media"]'
            ).find_elements_by_tag_name('a')
            gallary_div_a_tags[0].click()
            images_div = self.driver.find_element_by_class_name(
                'm6QErb.DxyBCb.kA9KIf.dS8AEf'
                )
            oldLength = 0
            while True:
                images_div.send_keys(Keys.END)
                sleep(1.5)
                all_images = images_div.find_elements_by_class_name('Uf0tqf.loaded')
                if(len(all_images) > self.images_needed - 1 or len(all_images) == oldLength):
                    break
                oldLength = len(all_images)
            all_images = images_div.find_elements_by_class_name('Uf0tqf.loaded')
            print("Total images: ",len(all_images))
            count = 1
            for image in all_images:
                style_attributes = str(image.get_attribute('style')).strip()
                style_attributes = style_attributes.split("background-image:",1)
                style_attributes = style_attributes[1].split('"',2)
                style_attributes = style_attributes[1]
                gallary_images += style_attributes + ' , \n'
                if(count == self.images_needed):
                    break
                count += 1
            print("Images scraped: ",count-1)
            print("Images char length: ",len(gallary_images))
        except:
            pass
        try:
            #going back to previous page
            self.driver.find_element_by_css_selector(
                'button[data-tooltip="Back"]'
            ).click()
        except:
            pass
        return gallary_images
