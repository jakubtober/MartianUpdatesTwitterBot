import time
import json
import requests
import imageio
from PIL import Image
from app_auth import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from twython import Twython
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

MARS_NASA_GOV = 'https://mars.nasa.gov/mars-exploration/overlay-curiosity/'
REAL_DATA_URL_REMS = (
    'http://cab.inta-csic.es/rems/wp-content/plugins/marsweather-widget/widget.php?lang=en'
)
TEST_DATA_URL_REMS = 'file:///home/jakub/Coders_lab/MartianUpdates/REMS%20Weather%20Widget.html'

# Waiting for x seconds before scraping as it takes some time to load data from
# server and to render widget/page etc
WAITING_TIME = 5

def initiate_selenium(url, time_to_wait):
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get(url)
    time.sleep(time_to_wait)
    return browser


class RoverData():

    def __init__(self):
        self.status_code_mars_gov = requests.get(MARS_NASA_GOV)
        self.status_code_mars_rems = requests.get(REAL_DATA_URL_REMS)

        if self.status_code_mars_gov.status_code != 200:
            print("Can't access MARS GOV data source...")

        if self.status_code_mars_rems.status_code != 200:
            print("Can't access MARS REMS data source...")

    def get_remaining_mars_rems_data(self):
        browser = initiate_selenium(REAL_DATA_URL_REMS, WAITING_TIME)
        data_not_exists = False

        if self.status_code_mars_rems.status_code != 200:
            print('Sorry, no REMS data available at the moment...')
            self.last_day_data = {}
        else:
            self.last_day_data = {
                'earths_date': browser.find_element_by_id('mw-terrestrial_date').text,
                'sol': browser.find_element_by_id('mw-sol').text,
                'air_temp_min': browser.find_element_by_id('mw-min_temp').text,
                'air_temp_max': browser.find_element_by_id('mw-max_temp').text,
                'ground_temp_min': browser.find_element_by_id('mw-min_gts_temp').text,
                'ground_temp_max': browser.find_element_by_id('mw-max_gts_temp').text,
                'pressure': browser.find_element_by_id('mw-pressure').text,
                'wind_speed': browser.find_element_by_id('mw-wind_speed').text,
                'humidity': browser.find_element_by_id('mw-abs_humidity').text,
                'sunrise_time': browser.find_element_by_id('mw-sunrise').text,
                'sunset_time': browser.find_element_by_id('mw-sunset').text,
                'atmospheric_opacity': browser.find_element_by_id('mw-atmo_opacity').text,
                'radiation_level': (
                    browser.find_element_by_id('mw-local_uv_irradiance_index')
                    .find_element_by_tag_name('span')
                    .get_attribute('title')
                ),
                }

            while data_not_exists:
                sol_no = browser.find_element_by_id('mw-sol').text

                data_file = open('mars_rems_data.json', 'r')
                data = json.load(data_file)

                # test if data already exists in the history, collect it if not
                if sol_no in list(data.keys()):
                    print("Looks like there is no new weather REMS data.")
                    data_not_exists = False
                else:
                    day_weather_data = {
                        'earths_date': browser.find_element_by_id('mw-terrestrial_date').text,
                        'sol': browser.find_element_by_id('mw-sol').text,
                        'air_temp_min': browser.find_element_by_id('mw-min_temp').text,
                        'air_temp_max': browser.find_element_by_id('mw-max_temp').text,
                        'ground_temp_min': browser.find_element_by_id('mw-min_gts_temp').text,
                        'ground_temp_max': browser.find_element_by_id('mw-max_gts_temp').text,
                        'pressure': browser.find_element_by_id('mw-pressure').text,
                        'wind_speed': browser.find_element_by_id('mw-wind_speed').text,
                        'humidity': browser.find_element_by_id('mw-abs_humidity').text,
                        'sunrise_time': browser.find_element_by_id('mw-sunrise').text,
                        'sunset_time': browser.find_element_by_id('mw-sunset').text,
                        'atmospheric_opacity': browser.find_element_by_id('mw-atmo_opacity').text,
                        'radiation_level': (
                            browser.find_element_by_id('mw-local_uv_irradiance_index')
                            .find_element_by_tag_name('span')
                            .get_attribute('title')
                        ),
                        }
                    data[sol_no] = day_weather_data
                    with open("mars_rems_data.json", "w") as write_file:
                        json.dump(data, write_file)
                    print('Data collected and added to database.')
                    print(day_weather_data)

                browser.find_element_by_id('mw-previous').click()
                time.sleep(2)
            browser.close()

    def get_time(self):
        browser = initiate_selenium(MARS_NASA_GOV, 2)

        # dirty time extraction straight form website
        self.location_and_time_str = (
            browser.find_element_by_class_name('current_location')
            .find_element_by_class_name('description')
            .text
        )
        time_str_list = self.location_and_time_str.split(' ')[:2]
        self.location_str = self.location_and_time_str.split('-')[1]
        self.time_str = self.location_and_time_str.split('-')[0]
        hour = int(time_str_list[0].split(':')[0])
        minutes = int(time_str_list[0].split(':')[1])
        am_pm = time_str_list[1]
        self.time = [hour, minutes, am_pm]

        self.present_sol_number = int(browser.find_element_by_class_name('time_years').text[:4])

        print((
            'Actual time collected. Present sol: {}. Local Mars time is: {}.'
            .format(self.present_sol_number, str(self.time)))
        )
        print('Location collected. Rover is in: {}'.format(self.location_str))
        browser.close()

    def get_photos(self, sol, cam):
        '''ROVER CAMERAS
        FHAZ	Front Hazard Avoidance Camera
        RHAZ	Rear Hazard Avoidance Camera
        MAST	Mast Camera
        CHEMCAM	Chemistry and Camera Complex
        MAHLI	Mars Hand Lens Imager
        MARDI	Mars Descent Imager
        NAVCAM	Navigation Camera
        '''

        api_endpoint = (
            'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/'
            'photos?sol={}&camera={}&api_key=DEMO_KEY'
            .format(sol, cam)
        )
        response = requests.get(api_endpoint)
        data = json.loads(response.text)
        no_of_photos = len(data['photos'])
        file_names = []
        print('Number of photos: {}'.format(no_of_photos))
        photo_id = 1
        for element in data['photos']:
            browser = initiate_selenium(element['img_src'], 2)
            photo_name_png = './photos/png/{}-{}-{}.png'.format(sol, cam, photo_id)
            photo_name_jpg = './photos//jpg/{}-{}-{}.jpg'.format(sol, cam, photo_id)
            browser.get_screenshot_as_file(photo_name_png)

            im = Image.open(photo_name_png)
            rgb_im = im.convert('RGB')
            rgb_im.save(photo_name_jpg)

            self.photo_file_names.append('{}-{}-{}.jpg'.format(sol, cam, photo_id))
            browser.close()
            print("Photos left: {}".format(no_of_photos - photo_id))
            photo_id += 1
