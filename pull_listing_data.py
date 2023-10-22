#This file has class and functions to pull data from listing page
from cmath import log
import imp
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
#import GMB.member_reviews as mr
import GMB.member_images as mi
import re
import secrets



class Listing():
    def __init__(self, driver:WebDriver ,listingURL, profession,location,lat,lon,previousCompany,user_id,counter):
        self.driver = driver
        self.driver.implicitly_wait(15)
        self.listing_url = listingURL
        self.profession = profession
        self.location = location
        self.oldCOmpany = previousCompany
        self.lat = lat
        self.lon = lon
        self.counter = counter
        self.linkedin = ''
        self.facebook = ''
        self.instagram = ''
        self.twitter = ''
        self.user_id = user_id
        self.listing_page_url = self.driver.current_url
        self.geolocator = Nominatim(user_agent="geoapiExercises")
        listing_data_column_names = const.LISTINGS_DATA
        self.listing_data = pd.DataFrame(columns=listing_data_column_names)
    
    def pull_social_urls(self):
        self.driver.implicitly_wait(0.5)
        try:
            social_urls_div = self.driver.find_element_by_css_selector(
                'div[data-attrid="kc:/common/topic:social media presence"]'                
            )
            social_a_tags = social_urls_div.find_elements_by_tag_name('a')
            for social_url in social_a_tags:
                href = str(social_url.get_attribute('href')).strip()
                if 'www.linkedin.com' in href:
                    self.linkedin = href
                elif 'www.facebook.com' in href:
                    self.facebook = href
                elif 'instagram.com' in href:
                    self.instagram = href
                elif 'twitter.com' in href:
                    self.twitter = href
        except:
            pass
        self.driver.implicitly_wait(15)



    def pull_listing_data(self):

        # getting 'data_pid_place_id','data_fid_data_id','data_cid','eid','data_ved','data_maps_rw_api_key'
        all_ids_div = self.driver.find_element_by_class_name("akp-el")
        data_fid_data_id = str(all_ids_div.get_attribute('data-fid')).strip()
        data_cid = str(all_ids_div.get_attribute('data-cid')).strip()
        eid = str(all_ids_div.get_attribute('eid')).strip()
        data_ved = str(all_ids_div.get_attribute('data-ved')).strip()
        pid_parent_div = self.driver.find_element_by_id("wrkpb")
        data_pid_place_id = str(pid_parent_div.get_attribute('data-pid')).strip()
        data_maps_rw_api_key = str(pid_parent_div.get_attribute('data-maps-rw-api-key')).strip()
        # pulling company name
        company = ""
        try:
            #while company == self.oldCOmpany:
                company = str(self.driver.find_element_by_css_selector(
                    'h2[data-attrid="title"]'
                ).find_element_by_tag_name('span').get_attribute('innerHTML')).strip()
                company = company.replace('&amp;','&')
        except:
            pass
        print("Getting Company Name: ",company)
        first_name = ""
        last_name = ""
        if(company != " "):
            company22 = company
            first_name = company
            last_name = " "
            if(company.count(' ')>0):
                company = company.split(" ",1)
                first_name = company[0]
                last_name = company[1]
                
            company = company22
        print("Getting first_name: ",first_name)
        print("Getting last_name: ",last_name)

        # this try and except will give us website URL of business
        website = ""
        try:
            website_button_div = self.driver.find_elements_by_class_name(const.WEBSITE_DIV_CLASS)
            for button in website_button_div:
                innerHTML = str(button.get_attribute('innerHTML')).strip()
                if 'Website' in innerHTML:
                    website = str(button.find_element_by_tag_name(
                        'a'
                    ).get_attribute('href')).strip()
        except:
            pass
        print("Getting website: ",website)

        # this try and except will give us the listing location
        address1 = ""
        city = ""
        state_code = ""
        country_code = ""
        zip_code = ""
        lat = self.lat
        lon = self.lon
        state_ln = ''
        country_ln = ''

        print('lat: ',lat,' lon: ',lon)
        try:
            address_div = self.driver.find_element_by_css_selector(
                'div[data-attrid="kc:/location/location:address"]'
            )
            address1 = str(address_div.find_element_by_class_name(
                const.ADDRESS_CLASS
                ).get_attribute('innerHTML')).strip()
            address1 = address1.replace('&amp;','&')
            country_code = 'US'
            country_ln = 'United States'
            self.driver.implicitly_wait(0.5)
            try:
                address_bits = address1.split(",", 3)
            except:
                pass
            try:
                state_zip = address_bits[-2].strip()
                state_zip = state_zip.split(" ",1)
                #print("Printing state: ", state_zip[0], "Printing zip: ",state_zip[1])
            except:
                pass
            try:
                city = address_bits[-3].strip()
            except:
                pass
            try:
                state_code = state_zip[0].strip()
                try:
                    state_ln = const.STATES[state_code]
                except:
                    pass
            except:
                pass
            try:
                zip_code = state_zip[1].strip()
            except:
                pass
        except:
            pass
        self.driver.implicitly_wait(15)

        print("Getting address: ",address1)
        print("Getting city: ",city)
        print("Getting state_code: ",state_code)
        print("Getting state_ln: ",state_ln)
        print("Getting country_code: ",country_code)
        print("Getting country_code: ",country_ln)
        print("Getting zip_code: ",zip_code)
        print("Getting lat: ",lat)
        print("Getting lon: ",lon)
        
        self.driver.implicitly_wait(0.5)
        phone_number = ""
        try:
            phone_number = str(self.driver.find_element_by_css_selector(
                'span[aria-label^="Call phone number"]'
            ).get_property('innerHTML')).strip()
            phone_number = phone_number.replace('&amp;','&')
        except:
            pass
        print("Getting Phone number: ",phone_number)
        self.driver.implicitly_wait(15)

        # getting working hours
        working_hours = ""
        try:
            working_hours_div = self.driver.find_element_by_css_selector(
                'div[data-attrid="kc:/location/location:hours"]'
            )
            more_button = working_hours_div.find_element_by_css_selector(
                'div[role="button"]'
            )
            more_button.click()

            time_table_rows = working_hours_div.find_element_by_class_name(
                "WgFkxc"
                ).find_elements_by_tag_name('tr')
            # making do while to get day and time instead of None
            #while True:
            #    time_table_rows.get
            for day in time_table_rows:
                td_tags = day.find_elements_by_tag_name('td')
                one_day = str(td_tags[0].get_attribute('innerHTML')).strip()
                time = str(td_tags[1].get_attribute('innerHTML')).strip()
                working_hours += one_day + "\t\t" + time + '\n'
        except:
            pass
        working_hours = working_hours.strip()
        print("Getting Working hours: \n",working_hours)

        # getting default logo of listing
        self.driver.implicitly_wait(0.5)
        logo = ""
        try:
            logo = str(self.driver.find_element_by_css_selector(
                'img[alt="Merchant logo"]'
            ).get_attribute('src')).strip()
            logo = logo.replace('&amp;','&')
        except:
            pass
        print("Getting Logo: ",logo)


        #Fetching social URLs
        
        self.pull_social_urls()
        
        print("facebook: ", self.facebook,'\nLinkedin: ', self.linkedin,)
        print("instagram: ", self.instagram,'\n twitter: ', self.twitter,)
        self.driver.implicitly_wait(15)

        filename =  re.sub('[^a-zA-Z0-9 \n\.]', '', company)
        filename = filename.replace(" ",'-')
        filename = filename.replace("--",'-')
        filename = f'{filename}'
        filename = filename.lower()

        #getting reviews of listing and storing in another csv
        #Reviews = mr.Reviews(self.driver,self.user_id,filename)
        
        #if(self.counter == 1):
        #     Reviews.pull_reviews().to_csv(f'{const.DIRECTORY_NAME}/reviews_{self.profession}_{self.location}.csv',index=False)
        #else:
        #    Reviews.pull_reviews().to_csv(f'{const.DIRECTORY_NAME}/reviews_{self.profession}_{self.location}.csv', mode='a', index=False, header=False)

        #getting reviews of listing and storing in another csv
        '''
        images = mi.Images(self.driver,self.user_id)
        gallary_phoros = images.pull_images()
        google_logo = gallary_phoros
        try:
            google_logo = google_logo.split(',',1)
            google_logo = str(google_logo[0]).strip()
        except:
            google_logo = ''
        '''
        self.driver.implicitly_wait(0.5)
        google_logo = ''
        try:
            #getting first gallary photo as google logo
            first_gallary_img = self.driver.find_element_by_class_name("vwrQge")
            google_logo = str(first_gallary_img.get_attribute('style')).strip()
            google_logo = google_logo.split("(",1)
            google_logo = google_logo[1].split(")",1)
            google_logo = google_logo[0].replace('"','')
        except:
            pass
        self.driver.implicitly_wait(5)
        
        #generating modtime for database
        modtime = str(datetime.today())
        modtime = modtime.split(".",1)
        modtime = modtime[0]
        

        signup_date = str(datetime.today())
        signup_date = signup_date.split('.',1)
        signup_date = signup_date[0]
        signup_date = signup_date
        signup_date = signup_date.replace('-','')
        signup_date = signup_date.replace(' ','')
        signup_date = signup_date.replace(':','')

        profession_id = const.CATEGORY_ID[self.profession]

        df2 = pd.DataFrame({'user_id':self.user_id,'listing_type':'Company','first_name':first_name,
        'last_name':last_name,'company':company,'phone_number':phone_number,'email':f'{self.user_id}@contractorsaz.com','address1':address1,'city':city,'zip_code':zip_code,
        'state_code':state_code,'state_ln':state_ln,'country_code':'US','country_ln':country_ln,'website':website,'facebook':self.facebook,'instagram':self.instagram,'twitter':self.twitter,'linkedin':self.linkedin,
        'password':'strongPassword@','lat':lat,'lon':lon,'rep_matters':working_hours,'modtime':modtime,'subscription_id':'9','filename':filename,'active':'2','token':secrets.token_hex(16),'signup_date':signup_date,'preferred':'0','verified':'0','nationwide':'0','parent_id':'0','geo_state':'0','profession_id':profession_id,'google_import':'1','google_url':self.driver.current_url,'google_logo':google_logo,'logo':logo,'data_pid_place_id':data_pid_place_id,'data_fid_data_id':data_fid_data_id,'data_cid':data_cid,'eid':eid,'data_ved':data_ved,'data_maps_rw_api_key':data_maps_rw_api_key},index=[0])


        self.listing_data = pd.concat([self.listing_data,df2], ignore_index=True)
        return self.listing_data

        self.driver.implicitly_wait(200)



            
        
       



