import imp
from lib2to3.pgen2 import driver
from operator import imod
from pickle import TRUE
from selenium import webdriver
import constants as const
from selenium.webdriver.chrome.options import Options
from prettytable import PrettyTable
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from selenium.common.exceptions import NoSuchElementException
import pull_reviews_data as mr
import shutil

class ReviewsResult(webdriver.Chrome):
    def __init__(self,tearDown = False,driver_path = const.DRIVER_PATH,File_name=''):
        self.driver_path = driver_path
        self.file_name = File_name
        print(File_name)
        options = Options()
        options.binary_location = const.APPLICATION_PATH
        #options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(ReviewsResult,self).__init__(executable_path=driver_path,options=options)
        self.implicitly_wait(5)
        self.maximize_window()
        self.oldCompany = ''
        self.company = ''
    def land_on_page(self,url):
        self.get(url)

    def land_on_default_page(self):
        self.get(const.WEB_URL)
        sleep(5)

    def quit_browser(self):
        self.quit()
    
    def last_scraped_reviews_listing_id(self):
        if (os.path.isfile(f'reviews_{self.file_name}.csv')):
            reviews_data = pd.read_csv(f'reviews_{self.file_name}.csv')
            last_row = reviews_data.iloc[-1:]
            return int(last_row['user_id'].iat[0])
        else:
            return 0

    def wait_for_listing_to_be_loaded(self):
        # pulling company name
                while self.company == self.oldCompany:
                    try:
                        self.company = str(self.find_element_by_css_selector(
                                'h2[data-attrid="title"]'
                            ).find_element_by_tag_name('span').get_attribute('innerHTML')).strip()
                        self.company = self.company.replace('&amp;','&')
                    except:
                        pass
                    
                self.oldCompany = self.company
    def check_if_reviews_exists(self):
        flag = True
        try:
            google_reviews_div = self.find_element_by_css_selector(
                    'div[data-attrid="kc:/local:lu attribute list"]'
                )
        except:
            flag = False
        return flag

    def pull_reviews_results(self):
        user_id = ''
        filename = ''
        os.chdir('/Users/zainali/scraping1/GMB listings 1/files')
        listing_data = pd.read_csv(self.file_name)
        listing_data = listing_data.reset_index()
        counter = 1
        total_listings = len(listing_data)
        last_scraped_user_id = self.last_scraped_reviews_listing_id()
        for index, listingURL in listing_data.iterrows():

            #checking to skip if already scraped reviews
            if(int(listingURL['user_id']) > last_scraped_user_id):
                #Opening listing
                print("\n\n\nOpening ID: ", listingURL['user_id'],' name: ',listingURL['company'],' from ', self.file_name)
                self.land_on_page(listingURL['google_url'])
                #sleep(5000)
                #if(counter % 10 == 0):
                #    self.refresh()

                self.wait_for_listing_to_be_loaded()
                if(self.company == listingURL['company']):
                    if(self.check_if_reviews_exists()):
                        #getting reviews of listing and storing in another csv
                        Reviews = mr.Reviews(self,listingURL['user_id'],listingURL['filename'])
                        #getting reviews of listing and storing in another csv
                        if(counter == 1):
                            Reviews.pull_reviews().to_csv(f'reviews_{self.file_name}.csv',index=False)
                            print("Saving reviews in csv file for ", listingURL['company'])
                        else:
                            Reviews.pull_reviews().to_csv(f'reviews_{self.file_name}.csv', mode='a', index=False, header=False)
                            print("Appending reviews in csv file for ", listingURL['company'])
                            counter += 1
                    else:
                        print("No reviews found for ", listingURL['user_id'],' name: ',listingURL['company'])
                else:
                    print("Company name did not match old = ", f"{listingURL['company']} != {self.company}")
            else:
                    print("Already scraped reviews till user_id: ",last_scraped_user_id)
                    print("Reviews already scraped for ", f"{listingURL['user_id']} :{listingURL['company']}")
                    counter += 1


            total_listings -= 1
            print("Remaining listing reviews: ", total_listings)

        #moving file to reviews scraped file folder
        target_dir = const.target_dir
        source_dir = const.source_dir
        shutil.move(os.path.join(source_dir, self.file_name), target_dir)
        shutil.move(os.path.join(source_dir, f'reviews_{self.file_name}.csv'), target_dir)
        

        