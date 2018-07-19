import time
import json
import requests
import imageio
from PIL import Image
from app_auth import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from twython import Twython
from selenium import webdriver

MARS_NASA_GOV = 'https://mars.nasa.gov/mars-exploration/overlay-curiosity/'
REAL_DATA_URL_REMS = 'http://cab.inta-csic.es/rems/wp-content/plugins/marsweather-widget/widget.php?lang=en'
TEST_DATA_URL_REMS = 'file:///home/jakub/Coders_lab/MartianUpdates/REMS%20Weather%20Widget.html'

# Select around 5-10 seconds when using real url as it takes longer to load data from server for the widget
# and to refresh widget
WAITING_TIME = 5


def initiate_selenium(url, time_to_wait):
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    driver.get(url)
    time.sleep(time_to_wait)
    return driver


def get_last_day_data():
    driver = initiate_selenium(REAL_DATA_URL_REMS, WAITING_TIME)
    mars_rems_data_actual_date = {
        'earths_date': driver.find_element_by_id('mw-terrestrial_date').text,
        'sol': driver.find_element_by_id('mw-sol').text,
        'air_temp_min': driver.find_element_by_id('mw-min_temp').text,
        'air_temp_max': driver.find_element_by_id('mw-max_temp').text,
        'ground_temp_min': driver.find_element_by_id('mw-min_gts_temp').text,
        'ground_temp_max': driver.find_element_by_id('mw-max_gts_temp').text,
        'pressure': driver.find_element_by_id('mw-pressure').text,
        'wind_speed': driver.find_element_by_id('mw-wind_speed').text,
        'humidity': driver.find_element_by_id('mw-abs_humidity').text,
        'sunrise_time': driver.find_element_by_id('mw-sunrise').text,
        'sunset_time': driver.find_element_by_id('mw-sunset').text,
        'atmospheric_opacity': driver.find_element_by_id('mw-atmo_opacity').text,
        'radiation_level': driver.find_element_by_id('mw-local_uv_irradiance_index').find_element_by_tag_name('span').get_attribute('title'),
        }
    driver.close()
    return mars_rems_data_actual_date


def get_whole_history_mars_rems_data():
    initiate_selenium(REAL_DATA_URL, 3)
    no_of_sols = int(driver.find_element_by_id('mw-sol').text)
    whole_mars_rems_history = {}
    for day in range(0, no_of_sols):
        try:
            sol = int(driver.find_element_by_id('mw-sol').text)
            whole_mars_rems_history[sol] = get_last_day_data()
        except:
            print("Sorry, {} data was not fully available...".format(sol))

        with open("mars_rems_data.json", "w") as write_file:
            json.dump(whole_mars_rems_history, write_file)

        print("Sols left: {}".format(no_of_sols - day))
        driver.find_element_by_id('mw-previous').click()
        time.sleep(2)
    return whole_mars_rems_history


def get_photos(sol, cam):
    '''ROVER CAMERAS
    FHAZ	Front Hazard Avoidance Camera
    RHAZ	Rear Hazard Avoidance Camera
    MAST	Mast Camera
    CHEMCAM	Chemistry and Camera Complex
    MAHLI	Mars Hand Lens Imager
    MARDI	Mars Descent Imager
    NAVCAM	Navigation Camera
    '''

    api_endpoint = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={}&camera={}&api_key=DEMO_KEY'.format(sol, cam)
    response = requests.get(api_endpoint)
    data = json.loads(response.text)
    no_of_photos = len(data['photos'])
    file_names = []
    print('Number of photos: {}'.format(no_of_photos))
    photo_id = 1
    for element in data['photos']:
        driver = initiate_selenium(element['img_src'], 2)
        photo_name_png = './photos/png/{}-{}-{}.png'.format(sol, cam, photo_id)
        photo_name_jpg = './photos//jpg/{}-{}-{}.jpg'.format(sol, cam, photo_id)
        driver.get_screenshot_as_file(photo_name_png)

        im = Image.open(photo_name_png)
        rgb_im = im.convert('RGB')
        rgb_im.save(photo_name_jpg)

        file_names.append('{}-{}-{}.jpg'.format(sol, cam, photo_id))
        driver.close()
        print("Photos left: {}".format(no_of_photos - photo_id))
        photo_id += 1
    return file_names


def get_time():
    driver = initiate_selenium(MARS_NASA_GOV, 2)
    time_and_location_str = driver.find_element_by_class_name('current_location').find_element_by_class_name('description').text
    time_str_list = time_and_location_str.split(' ')[:2]
    hour = int(time_str_list[0].split(':')[0])
    minutes = int(time_str_list[0].split(':')[1])
    am_pm = time_str_list[1]
    time = [hour, minutes, am_pm]
    driver.close()
    return time
