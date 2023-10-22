#This file has class and functions to pull data from listing page
from cmath import log
from tkinter.messagebox import ABORTRETRYIGNORE
from unicodedata import name
import pandas as pd
from lib2to3.pgen2 import driver
import constants as const
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep
from geopy.geocoders import Nominatim
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import secrets
import random
from selenium.webdriver.common.action_chains import ActionChains
import time, sys
import keyboard
import os




class Reviews():
    def __init__(self, driver:WebDriver ,user_id,file_name):
        self.driver = driver
        self.user_id = user_id
        self.file_name = file_name
        self.review_id = 0
        self.total_reviews = random.randint(5,15)
        reviews_column_names = const.REVIEWS_DATA
        self.reviews_data = pd.DataFrame(columns=reviews_column_names)
        os.chdir('/Users/zainali/scraping1/GMB listings 1/files')


        
    def update_review_id_in_file(self, review_id):
        with open(const.REVIEW_ID_TXT, 'w') as f:
            f.write(str(review_id))
            f.close()
    def read_review_id_from_file(self):
        with open(const.REVIEW_ID_TXT,mode='r') as f:
                self.review_id = int(f.readline())


    def pull_reviews(self):
        try:
            google_reviews_div = self.driver.find_element_by_css_selector(
                'div[data-attrid="kc:/local:lu attribute list"]'
            )
            #clicking on view google reviews
            self.driver.find_element_by_css_selector(
                'span[jscontroller="qjk5yc"]'
            ).click()

            #getting reviews div
            all_reviews_div = self.driver.find_element_by_class_name(
               "review-dialog-list"
            )
            
            all_reviews = all_reviews_div.find_elements_by_class_name('gws-localreviews__google-review')

            #checking actual total reviews 
            total_reviews_actual = str(self.driver.find_element_by_class_name(
                "z5jxId"
            ).get_attribute('innerHTML')).strip()
            total_reviews_actual = total_reviews_actual.split(' ',1)
            total_reviews_actual = total_reviews_actual[0].strip()
            total_reviews_actual = total_reviews_actual.replace(',','')
            total_reviews_actual = int(total_reviews_actual)
            self.total_reviews = total_reviews_actual # asking to store to get all reviews
            print("Total actual reviews: ", total_reviews_actual)

            #getting newest reviews first
            self.driver.find_element_by_css_selector('div[data-sort-id="newestFirst"]').click()
            sleep(2)


            all_reviews_div = self.driver.find_element_by_class_name("review-dialog-list"
            )
            while True:
                try:
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", all_reviews_div)
                    all_reviews = all_reviews_div.find_elements_by_class_name('gws-localreviews__google-review')
                    sys.stdout.write("\r" + "Scrolling Reviews " + str(len(all_reviews))+ ' of '+ str(self.total_reviews))
                    sys.stdout.flush()
                    if(len(all_reviews) == self.total_reviews or len(all_reviews) >= 1200):
                        break
                    if(str(self.user_id).strip() == '18563' and len(all_reviews) >= 670):
                        break
                except:
                    break 


            print('\n')
            self.driver.implicitly_wait(0.5)
            count = 0
            for review in all_reviews:
                
                self.read_review_id_from_file()
                #if(count == 0):
                #    self.driver.implicitly_wait(5)
                #else:
                #    self.driver.implicitly_wait(0.5)

                #getting user name
                user_name = str(review.find_element_by_class_name(
                    "TSUbDb"
                    ).find_element_by_tag_name('a').get_attribute('innerHTML')).strip()
                #print(user_name)
                #print("\nReview user name: ", user_name)

                #getting total rating
                star_rating = str(review.find_element_by_tag_name(
                    'g-review-stars'
                    ).find_element_by_tag_name('span').get_attribute('aria-label'))
                star_rating = star_rating.split('out',1)
                star_rating = star_rating[0].split(' ',1)
                star_rating = star_rating[1].strip()
                #print("Rating: ", star_rating)

                #getting review description, first clicking on read more for each reviews
                try:
                    review.find_element_by_class_name("review-more-link").click()
                except:
                    pass
                description_review = ""
                try:
                    description_review = str(review.find_element_by_class_name(
                        'review-full-text'
                    ).get_attribute('innerHTML')).strip()
                except:
                    try:
                        description_review = str(review.find_element_by_css_selector(
                        'span[tabindex="-1"]'
                    ).get_attribute('innerHTML')).strip()
                    except:
                        pass
                #print("Review Description: ", description_review)


                # getting review date
                days = 0
                month = 0
                year = 0
                all_reviews = all_reviews_div.find_elements_by_class_name('gws-localreviews__google-review')
                review_date = str(review.find_element_by_class_name(
                    "dehysf.lTi8oc"
                ).get_attribute('innerHTML')).strip()
                if('month' in review_date):
                    review_date = review_date.split(' ',1)
                    review_date = review_date[0].strip()
                    if(review_date == 'a'):
                        month = 1
                    else:
                        month = int(review_date)
                elif('week' in review_date):
                    review_date = review_date.split(' ',1)
                    review_date = review_date[0].strip()
                    if(review_date == 'a'):
                        days = 7
                    else:
                        days = int(review_date) * 7
                elif ('day' in review_date):
                    review_date = review_date.split(' ',1)
                    review_date = review_date[0].strip()
                    if(review_date == 'a'):
                        days = 1
                    else:
                        days = int(review_date)
                elif ('year' in review_date):
                    review_date = review_date.split(' ',1)
                    review_date = review_date[0].strip()
                    if(review_date == 'a'):
                        year = 1
                    else:
                        year = int(review_date)
                #print("Review Date: ", days, " days ", month, " month ", year, ' year ago')
                days_to_subtract = days + (30*month) + (365*year)
                revision_timestamp = str(datetime.today() - timedelta(days=days_to_subtract))
                revision_timestamp = revision_timestamp.split('.',1)
                revision_timestamp = revision_timestamp[0]
                #print("Review posted on: ",revision_timestamp)
                review_added = revision_timestamp
                review_added = review_added.replace('-','')
                review_added = review_added.replace(' ','')
                review_added = review_added.replace(':','')

                review_filename = self.file_name + '/writeareview'
                #print("Review posted on: ",review_added, ' ', revision_timestamp)
                df2 = pd.DataFrame({'review_id':self.review_id,'user_id':self.user_id,'review_description':description_review,'review_name':user_name,'review_email':f'{self.review_id}@123local.com','review_status':'2','review_added':review_added,'httpr':review_filename,'member_id':'0','review_token':secrets.token_hex(16),'review_updated':review_added,'rating_overall':star_rating,'rating_service':star_rating,'rating_response':star_rating,'rating_expertise':star_rating,'rating_results':star_rating,'spoken_language':'1','gender':'male','rating_language':star_rating,'recommend':'0','revision_timestamp':revision_timestamp,'formname':'member_review'},index=[0])

                self.reviews_data = pd.concat([self.reviews_data,df2], ignore_index=True)   
                self.update_review_id_in_file(review_id= (self.review_id+1))

                if(count >= self.total_reviews or count >= 1200):
                    break
                sys.stdout.write("\r" + "scrapped Reviews " + str(count)+ ' of '+ str(len(all_reviews)))
                sys.stdout.flush()
                count += 1


            self.driver.implicitly_wait(15)
            #closing the reviews section
            self.driver.execute_script("window.history.go(-1)")
        except:
            raise
        print("\nTotal reviews scraped: ", count, ' of ', self.total_reviews)
        return self.reviews_data