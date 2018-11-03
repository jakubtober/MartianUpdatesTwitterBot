import time
import json
import requests
import imageio
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from app_auth import (
    APP_KEY,
    APP_SECRET,
    OAUTH_TOKEN,
    OAUTH_TOKEN_SECRET,
    API_PASSWORD,
    API_USERNAME
)
from app_auth import (
    API_USERNAME,
    API_PASSWORD,
)


MARS_NASA_GOV = 'https://mars.nasa.gov/mars-exploration/overlay-curiosity/'
REAL_DATA_URL_REMS = (
    'http://cab.inta-csic.es/rems/wp-content/plugins/marsweather-widget/widget.php?lang=en'
)
TEST_DATA_URL_REMS = 'file:///home/jakub/Coders_lab/MartianUpdates/REMS%20Weather%20Widget.html'
WAITING_TIME = 5


def time_now():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ')


def initiate_selenium(url, time_to_wait):
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(
        options=options, executable_path='/usr/lib/chromium-browser/chromedriver')
    browser.get(url)
    time.sleep(time_to_wait)
    return browser


class ApiConnetction():
    AUTH_URL = 'http://jakubtober.pythonanywhere.com/api/token-auth/'
    GET_URL = 'http://jakubtober.pythonanywhere.com/api/sols/'
    CREATE_URL = 'http://jakubtober.pythonanywhere.com/api/sols/create/'

    def __init__(self):
        try:
            self.my_file = open('mars_rems_data.json')
            self.my_json = json.load(self.my_file)
        except Exception as error:
            raise error

        try:
            data = {
                'username': API_USERNAME,
                'password': API_PASSWORD
            }
            self.response = requests.post(self.AUTH_URL, data)
            self.token = self.response.json()['token']
        except Exception as error:
            raise error

    def __len__(self):
        return len(self.my_json)

    @property
    def auth_headers(self):
        my_auth_headers = {
            'Authorization': 'Token {}'.format(self.token)
        }
        return my_auth_headers

    def get_single_sol_json_file(self, sol_number):
        return self.my_json[str(sol_number)]

    def add_single_sol_to_api(self, sol_number):
        data_to_add = self.get_single_sol_json_file(sol_number)

        if self.token:
            check_sol_exists_response = requests.get(self.GET_URL + str(sol_number))
            if check_sol_exists_response.status_code != 200:
                response = requests.post(self.CREATE_URL, data=data_to_add,
                                         headers=self.auth_headers)
                return True
            else:
                return False

    def add_all_sols_to_api(self):
        for counter, sol_number in enumerate(self.my_json):
            if self.add_single_sol_to_api(sol_number):
                print('Sols left: ' + str(len(self.my_json) - counter))
            else:
                print('Sol {} not added - already in the database, or data incorrect'.format(sol_number))


class RoverDataScraper():
    def __init__(self):
        self.status_code_mars_gov = requests.get(MARS_NASA_GOV).status_code
        self.status_code_mars_rems = requests.get(REAL_DATA_URL_REMS).status_code

        if self.status_code_mars_gov != 200:
            print(time_now() + "can't access MARS GOV data source...")

        if self.status_code_mars_rems != 200:
            print(time_now() + "can't access MARS REMS data source...")

    def scrap_single_sol_data(self, browser):
        """Scrap single sol REMS data."""
        sol_data = {
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
        return sol_data

    def scrap_missing_sols_data(self):
        """Scrap REMS data for sols that are not in the database yet."""
        data_not_exists = True

        if self.status_code_mars_rems != 200:
            print(time_now() + 'sorry, no REMS data available at the moment...')
            self.last_day_data = {}
        else:
            browser = initiate_selenium(REAL_DATA_URL_REMS, WAITING_TIME)
            self.last_day_data = self.scrap_single_sol_data(browser)

            while data_not_exists:
                sol_no = browser.find_element_by_id('mw-sol').text

                data_file = open('mars_rems_data.json', 'r')
                data = json.load(data_file)

                if sol_no in list(data.keys()):
                    print(time_now() + "looks like there is no new weather REMS data.")
                    data_not_exists = False
                else:
                    day_weather_data = self.scrap_single_sol_data(browser)
                    data[sol_no] = day_weather_data
                    with open("mars_rems_data.json", "w") as write_file:
                        json.dump(data, write_file)
                    print(time_now() + 'data for sol {} collected and added to database.'.format(sol_no))

                    my_api_connection = ApiConnetction()
                    my_api_connection.add_single_sol_to_api(sol_no)
                    print(time_now() + 'data for sol {} added to API.'.format(sol_no))

                browser.find_element_by_id('mw-previous').click()
                time.sleep(2)
            browser.close()

    def get_time(self):
        if self.status_code_mars_gov != 200:
            self.location_and_time = ''
            self.location_str = ''
            self.time_str = ''
            self.time = []
        else:
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
                time_now() + 'actual time collected. Present sol: {}. Local Mars time is: {}.'
                .format(self.present_sol_number, str(self.time)))
            )
            print(time_now() + 'location collected. Rover is in: {}'.format(self.location_str))
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
        print(time_now() + 'number of photos: {}'.format(no_of_photos))
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
