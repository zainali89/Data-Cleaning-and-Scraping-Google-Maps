import imp
import pandas as pd

# This function will read categories from csv file and store in dataframe
def read_categories(path):
    df = pd.read_csv(path)
    list = df['categories'].tolist()
    return list


DRIVER_PATH = "/Users/zainali/scraping1/GMB listings 1/chromedriver"
APPLICATION_PATH = "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"
target_dir = '/Users/zainali/scraping1/GMB listings 1/files/Reviews Scraped files'
source_dir = '/Users/zainali/scraping1/GMB listings 1/files'

WEB_URL = "https://www.google.com/search?q=Air+conditioning+contractor+in+arizona&rlz=1C5GCEA_enPK991PK991&biw=1440&bih=789&tbm=lcl&sxsrf=ALiCzsae_J-TegN9qzl2UXJBGNHg-HleHw%3A1659023093335&ei=9a7iYpaEFL2S9u8P04m1kAY&oq=Air+conditioning+contractor+in+arizona&gs_l=#rlfi=hd:;si:;mv:[[33.7345389,-111.6487076],[33.3072932,-112.43172969999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:14"
PARENT_CATEGORY = 'Accommodation'
file_path = '/Users/zainali/scraping1/GMB listings 1/joseph/GMB Contractor Categories.csv'
CATEGORIES_LIST = []
CATEGORIES_LIST = read_categories(file_path)
LOCATION_LIST = ['Arizona']
NUMBER_OF_THREADS = 6
#LISTING_PER_CATEGORY =  150
DIRECTORY_NAME = 'files'
WEBSITE_DIV_CLASS = "QqG1Sd" #listing website div class
LISTING_DIV_JSNAME = "GZq3Ke" #search result 
ADDRESS_CLASS = "LrzXr"
LAT_LON_JSNAME = "xwKrYc"
PAGINATION_JSNAME = "TeSSVd"


#LISTINGS_DATA = ['user_id', 'modtime','listing_type','google_logo','logo',
#       'first_name','last_name','company',	'phone_number', 'email', 'address1', 'city',	'zip_code','state_code','state_ln','country_code','country_ln','website', 'facebook', 'linkedin', 'twitter', 'instagram', 'password','profession_id','rep_matters','lat','lon','subscription_id','filename','active','geo_state','nationwide','parent_id','preferred','signup_date','token','verified','google_import','google_url','gallary_phoros']

LISTINGS_DATA = ['user_id',	'first_name',	'last_name',	'email',	'company',	'phone_number',	'fax_number',	'address1',	'address2',	'city',	'zip_code',	'state_code',	'state_ln',	'country_code',	'country_ln',	'website',	'twitter',	'youtube',	'facebook',	'linkedin',	'blog',	'quote',	'experience',	'affiliation',	'awards',	'published',	'education',	'software',	'fees',	'about_me',	'featured',	'modtime',	'subscription_id',	'filename',	'box_style',	'password',	'active',	'token',	'ref_code',	'signup_date',	'cookie',	'page_title',	'last_login',	'testimonial',	'position',	'instagram',	'credentials',	'bitly',	'preferred'	,'profession_id'	,'facebook_id',	'google_id'	,'facebook_username'	,'facebook_email'	,'verified'	,'pre_hold',	'link',	'pinterest',	'nationwide',	'cv',	'work_experience'	,'rep_matters',	'speaking_engagements'	,'current_positions',	'gmap'	,'additional_fields'	,'video'	,'keywords',	'google_plus',	'listing_type',	'phone_number2',	'lat',	'lon',	'parent_id',	'no_geo',	'user_consent',	'place_id',	'opening_hours',	'price_level',	'google_rating',	'google_user_ratings_total',	'geo_state',	'search_description',	'google_logo',	'google_import',	'google_url',	'gallary_phoros',	'logo','data_pid_place_id','data_fid_data_id','data_cid','eid','data_ved','data_maps_rw_api_key']

REVIEWS_DATA = ['review_id','user_id','review_title','review_description','review_worked','service_id','review_name','review_email','review_zip','review_status','review_added','review_approved','ip','cookie','httpr','member_id','review_token','review_updated','rating_overall','rating_service','rating_response','rating_expertise','rating_results','spoken_language','gender','rating_language','recommend','review_company','revision_timestamp','formname','user_consent']

STATES = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}

USER_ID_TXT = '/Users/zainali/scraping1/GMB listings 1/user_id.txt'
REVIEW_ID_TXT = '/Users/zainali/scraping1/GMB listings 1/Scrape Reviews/review_id.txt'
