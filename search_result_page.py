import imp
from lib2to3.pgen2 import driver
from operator import imod
from pickle import TRUE
from selenium import webdriver
from GMB import pull_listing_data
import GMB.constants as const
from selenium.webdriver.chrome.options import Options
from prettytable import PrettyTable
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from selenium.common.exceptions import NoSuchElementException


class SearchResult(webdriver.Chrome):
    def __init__(self,tearDown = False,driver_path = const.DRIVER_PATH, prof="",loc=""):
        self.driver_path = driver_path
        self.teardown = tearDown
        self.profession = prof
        self.location = loc
        options = webdriver.ChromeOptions()
        options.binary_location = const.APPLICATION_PATH
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(SearchResult,self).__init__(executable_path=driver_path,options=options)
        self.implicitly_wait(5)
        self.maximize_window()

    def land_on_page(self):
        self.get(const.WEB_URL)

    def search(self,cat,loc):
        try:
            search_box = self.find_element_by_css_selector(
                'input[title="Search"]'
            )
            search_box.clear()
        except NoSuchElementException:
            self.refresh()
            search_box = self.find_element_by_css_selector(
                'input[title="Search"]'
            )
            search_box.clear()

        search_word = f'{cat} in {loc}'
        print('Searching for ', search_word)

        search_box.send_keys(search_word)
        search_btn = self.find_element_by_css_selector(
            'button[value="Search"]'
        )    
        search_btn.click()
    def quit_browser(self):
        self.quit()
    def update_user_id_in_file(self, user_id):
        with open(const.USER_ID_TXT, mode='w') as f:
            f.write(str(user_id))
            f.close()
    def pull_search_results(self):
        keyword = self.profession + ' in ' + self.location

        #getting search result boxes parent div
        results_div = self.find_element_by_id('search')

        #getting individual listing boxes in a list
        all_listing_boxes = results_div.find_elements_by_css_selector(
                'div[role="heading"]'
            )    
        print('Total listings: ',len(all_listing_boxes))

        #selecting pagination parent table row <tr>
        table_row = self.find_element_by_css_selector(
            f'tr[jsname={const.PAGINATION_JSNAME}]'
        )
        total_pages = len(table_row.find_elements_by_tag_name('td')) - 2 # getting total pages, 
        # did -2 because it has next and previous button too
        #iterating over all pages using pagination
        current_page = 0
        oldCompany = ""
        company = ''
        with open(const.USER_ID_TXT,mode='r') as f:
            user_id = int(f.readline())
        counter = 1

        skip_listing = 0
        #checking to skip some results already scraped
        if (os.path.isfile(f'{const.DIRECTORY_NAME}/{self.profession}_{self.location}.csv')):
                df_temp = pd.read_csv(f'{const.DIRECTORY_NAME}/{self.profession}_{self.location}.csv')
                skip_listing = len(df_temp)
        print("Listings to skip: ", skip_listing)

        while True:
            print('\n\n\n\nScraping page number ', current_page + 1,' for ', keyword)

            #getting search result boxes parent div
            sleep(5)
            results_div = self.find_element_by_id('search')

            #getting individual listing boxes in a list
            all_listing_boxes = results_div.find_elements_by_css_selector(
                    f'div[jsname={const.LISTING_DIV_JSNAME}]'
                )
            

            # iterating over search result boxes one by one to get data
            for listing_box in all_listing_boxes:
                print(f'\n\n\n\nScraping listing {counter} page {current_page + 1} for {keyword}')
                print('user_id: ', user_id)
                #getting individual listing boxes in a list
                results_div = self.find_element_by_id('search')
                all_listing_boxes = results_div.find_elements_by_css_selector(
                    f'div[jsname={const.LISTING_DIV_JSNAME}]'
                )
                #fetching lat and lon
                #if(current_page >= 14):
                lat = " "
                lon = " "
                try:
                    self.implicitly_wait(5)
                    lat = str(listing_box.find_element_by_css_selector(
                        'div[data-lat*="."]'
                    ).get_attribute('data-lat')).strip()
                    lon = str(listing_box.find_element_by_css_selector(
                        'div[data-lng*="."]'
                    ).get_attribute('data-lng')).strip()
                    self.implicitly_wait(3600)
                except:
                   pass
                    #print('lat: ',lat,' lon: ',lon)

                    #WebDriverWait(self, 2).until(
                    #    EC.element_to_be_clickable((By.CSS_SELECTOR,'div.role="heading"')))
                    
                    #Checking if restaurant is temporary closed or not
                listing_title_div = listing_box.find_element_by_class_name("dbg0pd.eDIkBe")
                innerHTML = str(listing_box.get_attribute('innerHTML')).strip()
                if(not 'Temporarily closed' in innerHTML) and skip_listing <= 0:
                    listing_title_div.click()
                    flagg = True
                    flagg_counter = 0
                    # pulling company name
                    while company == oldCompany:
                        try:
                                company = str(self.find_element_by_css_selector(
                                    'h2[data-attrid="title"]'
                                ).find_element_by_tag_name('span').get_attribute('innerHTML')).strip()
                                company = company.replace('&amp;','&')
                        except:
                            listing_title_div.click()
                        if(flagg_counter >= 200):
                            flagg = False
                        flagg_counter += 1
                    if not flagg:
                        continue

                    print('Old Company: ', oldCompany, ' New Company: ',company)
                    Listing = pull_listing_data.Listing(
                        driver = self,listingURL = self.current_url, profession = self.profession,
                        location = self.location,lat=lat, lon=lon, previousCompany= oldCompany,user_id=user_id,counter=counter
                        )
                    if(counter == 1):
                        Listing.pull_listing_data().to_csv(f'{const.DIRECTORY_NAME}/{self.profession}_{self.location}.csv',index=False)
                    else:
                        Listing.pull_listing_data().to_csv(f'{const.DIRECTORY_NAME}/{self.profession}_{self.location}.csv', mode='a', index=False, header=False)
                    
                    oldCompany = company
                    user_id += 1
                    self.update_user_id_in_file(user_id)
                else:
                    print("Listing is Temporarily closed or already scraped ",skip_listing)
                
                skip_listing -= 1
                counter += 1
                
                #sleep(2)
                
            print(" incrementing current_page ")
            current_page += 1
            try:
                print(" Going to next page ", current_page + 1)
                next_button = self.find_element_by_id("pnnext")
                #clicking on search button again
                self.find_element_by_css_selector('button[value="Search"]').click()
                #going to next page 
                self.find_element_by_css_selector(f'a[aria-label="Page {current_page + 1}"]').click()
                print("Clicked page ",current_page + 1)
                #next_button.click()
                #self.refresh()
                #sleep(2)
            except:
                break



        