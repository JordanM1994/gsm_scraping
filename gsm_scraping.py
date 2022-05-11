# -------------------------------------- Imports -----------------------------------------------#

import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import csv
import re

# -------------------------------------- User input for phone name -------------------------------------------#

phone_chosen = input("What phone are you looking for? ").lower()
phone_chosen_amended = phone_chosen.replace(" ", "_")
phone_model_key = phone_chosen.replace(" ", "-").upper()

url = "https://www.gsmarena.com/"

chrome_driver_path = "/Users/jordanmcleod/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# -------------------------------------- Finding device page -----------------------------------------------#

driver.get(url)
time.sleep(5)

# If a popup appears that requests you to accept cookies, this will accept, if it doesn't appear this step will skip.
try:
    agree = driver.find_element(by=By.XPATH, value='//*[@id="unic-b"]/div/div/div/div[3]/div[1]/button[2]')
    agree.click()
except NoSuchElementException:
    pass

time.sleep(2)

# Finds the search bar
search = driver.find_element(by=By.XPATH, value='//*[@id="topsearch-text"]')
search.send_keys(phone_chosen)
search.send_keys(Keys.ENTER)

time.sleep(3)

try:
    phone_link = driver.find_element(by=By.CSS_SELECTOR, value=f"a[href*={phone_chosen_amended}-]")
    phone_link.click()
except NoSuchElementException:
    phone_link = driver.find_element(by=By.CSS_SELECTOR, value=f"a[href*={phone_chosen_amended}]")
    phone_link.click()


time.sleep(3)

# ------------------------ All config for devices ---------------------------------------------------#

# -------------------------------------- 5g -----------------------------------------------#

if "5G" in driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[1]/tbody/tr[1]/td[2]/a').text:
    five_g = 1
    five_g_vector = "Ready for super-fast <strong>5G</strong> data"
else:
    five_g = 0
    five_g_vector = ""

# -------------------------------------- Release Year and Quarter -----------------------------------------------#


release_year_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[2]/tbody/tr[2]/td[2]').text
release_year = re.search('[0-9][0-9][0-9][0-9]', release_year_data)

# Release Quarter Data
rqd = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[2]/tbody/tr[2]/td[2]').text.lower()

release_quarter = 0

if "january" in rqd or "february" in rqd or "march" in rqd:
    release_quarter = 1
elif "april" in rqd or "may" in rqd or "june" in rqd:
    release_quarter = 2
elif "july" in rqd or "august" in rqd or "september" in rqd:
    release_quarter = 3
elif "october" in rqd or "november" in rqd or "december" in rqd:
    release_quarter = 4

# -------------------------------------- Operating System -----------------------------------------------#

# Try - allows script to run if the OS section cannot be found on the page
try:
    operating_system_data = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[5]/tbody/tr[1]/td[2]').text

    operating_system = operating_system_data.split(",")[0][:-2]

    # if statement changes amends the text to be lowercase for the Attribute Model
    if "Android" in operating_system_data:
        os = "android"
    elif "iOS" in operating_system_data:
        os = "apple_ios"
    else:
        os = operating_system_data.split(",")[0].lower()

# If the OS cannot be found on GSM Arena the field is set to ""
except NoSuchElementException:
    operating_system = ""
    os = ""

# -------------------------------------- UK/US Dimensions and weight -----------------------------------------------#

dimensions_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[1]/td[2]').text
weight_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[2]/td[2]').text

# captures the measurements in mm and the weight in grams
if "Unfolded" in dimensions_data.split("(")[0]:
    dimensions_uk = dimensions_data.split("(")[0].replace("Unfolded: ", "")
else:
    dimensions_uk = dimensions_data.split("(")[0]

# Some UK weights have 2 weights that are a gram apart, this checks if the device has more than one
# weight and selects the first
if "or" in weight_data:
    weight_uk = weight_data.split("(")[0].split("or")[0]
else:
    weight_uk = weight_data.split("(")[0]

# captures the measurements in inches and the weight in oz
try:
    dimensions_us = dimensions_data.split("(")[1]
except IndexError:
    dimensions_us = ""

weight_us = re.search('[0-9][.][0-9][0-9][ ][o][z]', weight_data)

# ------------------------------------------------ Water resistance ---------------------------------------------------#
# Catches the values of the Water resistance, if ip is in the text it will gather the data and format like : ipXX
# otherwise if the phrase water-repellent coating is caught it will add that, alternatively 0 will be returned.

try:
    water_resistance_data = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[3]/tbody/tr[4]/td[2]').text.lower()
    if "ip" in water_resistance_data:
        water_resistance = re.search('[i][p][0-9][0-9]', water_resistance_data).group()
    elif "water-repellent coating" in water_resistance_data:
        water_resistance = "water-repellent coating"
    else:
        water_resistance = 0
except NoSuchElementException:
    water_resistance = 0

# ------------------------------------------------ Touchscreen --------------------------------------------------------#

# Hard coded yes as almost all new phones are touchscreen
touchscreen = "Yes"

# -------------------------------------- Screen, Screen Size and resolution -------------------------------------------#

screen_size = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[4]/tbody/tr[2]/td[2]').text.replace(" inches", '"').split(",")[0]

# Catches the times when there is more than sentence in the resolution data
resolution_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text
if "," in resolution_data:
    resolution = resolution_data.split(",")[0]
else:
    resolution = resolution_data.split(" (")[0]


display_type = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[4]/tbody/tr[1]/td[2]').text.split(",")[0]

ppi = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text.split("~")[1].replace(" density)", '')

# -------------------------------------- Rear Cameras  -------------------------------------------#

# Gathers the number of cameras i.e. Single, Double, Triple or Quadruple

camera = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[1]/td[1]/a').text

# Gathers info for attribute model advanced info, dual camera if yes 1, no 0
if camera == "Single":
    dual_camera = 0
else:
    dual_camera = 1

# Gets the number of MP per camera and adds them to the camera section above

camera_data = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[7]/tbody/tr[1]/td[2]').text.split("\n")
for n in camera_data:
    split = n.split(",")
    camera += f" {split[0]} +"

# Gets information on the flash type i.e. LED Flash or Dual LED Flash

flash_type = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[7]/tbody/tr[2]/td[2]').text.split(",")[0]

# -------------------------------------- Front Cameras  -------------------------------------------#

# When the front camera is a single camera it will only display the MP of the camera, if there are dual or more this
# will output the number of cameras and the MP

if driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[1]/a').text == "Single":
    front_camera = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[2]').text.split(",")[0]
    front_camera_attribute = front_camera.split(" ")[0]
else:
    front_camera = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[1]/a').text
    front_cameras = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[2]').text.split("\n")
    for cam in front_cameras:
        split = cam.split(",")
        front_camera += f" {split[0]} +"

    front_camera_attribute = driver.find_element(
            by=By.XPATH,
            value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[2]').text.split(",")[0].split(" ")[0]

# No devices I could find have a selfie flash, hardcoded to 0
front_flash = 0

# -------------------------------------- OIS  -------------------------------------------#

ois_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[1]/td[2]').text.lower()
if "ois" in ois_data:
    ois = 1
else:
    ois = 0

# -------------------------------------- Camera Aperture  -------------------------------------------#

# Looking for f/X.X if it cannot find this it will set main_camera_aperture to ""

try:
    main_camera_aperture = re.search('[f][/][0-9][.][0-9]', ois_data).group()
except NoSuchElementException:
    main_camera_aperture = ""

# -------------------------------------- Pixel Size  -------------------------------------------#

try:
    pixel_size = re.search('[0-9][.][0-9][µ][m]', ois_data).group()[:-2]
except NoSuchElementException:
    pixel_size = ""

# -------------------------------------- Video Recording  -------------------------------------------#

# Gets information on the video recoding for the all handset database

video_recording = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[7]/tbody/tr[3]/td[2]').text.split(",")[0]

# Gets numerical data on the video recoding for the attribute model

video_recording_attribute_data = video_recording.split('@')[0].lower()
if "k" in video_recording_attribute_data:
    video_recording_attribute = int(video_recording_attribute_data[0])*1000
else:
    video_recording_attribute = int(video_recording_attribute_data.split("p")[0])

# -------------------------------------- Internal Storage  -------------------------------------------#

internal_storage = ""

# collects the various storage amounts and formats them like so: xxxGB/xxxGB/xxxTB

internal_storage_data = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[6]/tbody/tr[2]/td[2]').text.split(",")
for storage in internal_storage_data:
    if storage[0] == " ":
        split = storage[1:].split(" ")[0]
    else:
        split = storage.split(" ")[0]
    if split in internal_storage:
        pass
    else:
        internal_storage += f"{split}/"

# -------------------------------------- Cores and processor speeds ---------------------------------------------------#

# Try - allows script to run if the OS section cannot be found on the page, if the no_of_cores cannot be found it will
# set the value at ""

try:
    no_of_cores = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[5]/tbody/tr[3]/td[2]').text.split("(")[0]
except NoSuchElementException:
    no_of_cores = ""

processor = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[5]/tbody/tr[2]/td[2]').text.split("(")[0]

# The below tries to find the processor speed elements, if it can't, it simply sets to ""
# If it can find data it then formats the response to the following - XxX.XX x XxX.XX GHz

try:
    processor_speed_data = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[5]/tbody/tr[3]/td[2]').text.split("\n")
except NoSuchElementException:
    processor_speed_data = ""

if processor_speed_data == "":
    processor_speed = ""
else:
    processor_speed_list = re.findall('[0-9][x][0-9][.][0-9]*', processor_speed_data[0])
    processor_speed = ""
    for n in range(len(processor_speed_list)):
        if n+1 == len(processor_speed_list):
            processor_speed += f"{processor_speed_list[n]} GHz"
        else:
            processor_speed += f"{processor_speed_list[n]} x "

# -------------------------------------- Memory Cards and Sim Cards ---------------------------------------------------#


memory_card = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[6]/tbody/tr[1]/td[2]').text

# The position of the Sim card data can change so this tries the first location and if there is nothing there it moves
# to the next location.

try:
    sim_card = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[4]/td[2]').text
    if "Nano" in sim_card:
        sim_card = "Nano"
    elif "micro" in sim_card:
        sim_card = "Micro"
    else:
        sim_card = "Standard"
except NoSuchElementException:
    sim_card = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[3]/td[2]').text
    if "Nano" in sim_card:
        sim_card = "Nano"
    elif "micro" in sim_card:
        sim_card = "Micro"
    else:
        sim_card = "Standard"

# -------------------------------------- RAM  -------------------------------------------------------------#

# collects the various RAM amounts and formats them like so: xxxGB/xxxGB

ram = ""
ram_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[6]/tbody/tr[2]/td[2]').text.split(",")
for rams in ram_data:
    if rams[0] == " ":
        split = rams[1:].split(" ")[1]
    else:
        split = rams.split(" ")[1]
    if split in ram:
        pass
    else:
        ram += f"{split}/"

# -------------------------------------- Positioning  -------------------------------------------------------------#

positioning = driver.find_element(
    by=By.XPATH,
    value='//*[@id="specs-list"]/table[10]/tbody/tr[3]/td[2]').text.split("with ")[1]

# -------------------------------------- Radio  -------------------------------------------------------------#
radio_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[5]/td[2]').text
if "Unspecified" in radio_data:
    radio = "No"
else:
    radio = radio_data

# -------------------------------------- Internet  -------------------------------------------------------------#

internet = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[1]/td[2]').text
if "Wi-Fi" in internet:
    internet = "Yes"
else:
    internet = "No"

# -------------------------------------- WiFi  -------------------------------------------------------------#

wifi = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[1]/td[2]').text
if "Wi-Fi" in wifi:
    wifi = "Yes"
else:
    wifi = "No"

# -------------------------------------- Bluetooth  -------------------------------------------------------------#

bluetooth = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[2]/td[2]').text
if bluetooth == "No":
    bluetooth = "No"
else:
    bluetooth = "Yes"

# -------------------------------------- Hotspot  -------------------------------------------------------------#

hotspot = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[1]/td[2]').text
if "hotspot" in hotspot:
    hotspot = "Yes"
else:
    hotspot = "No"

# -------------------------------------- NFC  -------------------------------------------------------------#

if "yes" in driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[4]/td[2]').text.lower():
    other = "NFC"
    nfc = 1
else:
    other = ""
    nfc = 0

# -------------------------------------- Battery  -------------------------------------------------------------#

battery_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[12]/tbody/tr[1]/td[2]').text
battery = re.search(r'\b\d+\b', battery_data)

# -------------------------------------- Wireless Charging -------------------------------------------------#
# Checks to see if the device has wireless charging, if so 1 otherwise 0

try:
    wireless_charging_data = driver.find_element(
        by=By.XPATH,
        value='//*[@id="specs-list"]/table[12]/tbody/tr[2]/td[2]').text
    if "wireless charging" in wireless_charging_data.lower():
        wireless_charging = 1
    else:
        wireless_charging = 0
except NoSuchElementException:
    wireless_charging = 0

# -------------------------------------- CSV Export of data collected -------------------------------------------------#

# -------------------------------------- Headers of CSV  -------------------------------------------------------------#

headers = [
    "model_key",
    "phone_chosen",
    "operating_system",
    "dimensions",
    "weight",
    "touchscreen",
    "screen_size",
    "resolution",
    "ppi",
    "display_type",
    "camera",
    "video_recording",
    "flash_type",
    "front_camera",
    "internal_storage",
    "no_of_cores",
    "processor",
    "processor_speed",
    "memory_card",
    "sim_card",
    "ram",
    "positioning",
    "radio",
    "internet",
    "wifi",
    "bluetooth",
    "hotspot",
    "other",
    "battery",
    "standbytime",
    "talktime",
    "apps",
]

# -------------------------------------- UK Device Config -------------------------------------------------------------#

device_configuration_uk = [
    phone_model_key,
    phone_chosen,
    operating_system,
    dimensions_uk,
    weight_uk,
    touchscreen,
    screen_size,
    resolution,
    ppi,
    display_type,
    camera[:-2],
    video_recording,
    flash_type,
    front_camera,
    internal_storage[:-1],
    no_of_cores,
    processor,
    processor_speed,
    memory_card,
    sim_card,
    ram[:-1],
    positioning,
    radio,
    internet,
    wifi,
    bluetooth,
    hotspot,
    other,
    f"{battery.group()} mAh",
    "",
    "",
    "Yes"
]

# -------------------------------------- US Device Config -------------------------------------------------------------#

device_configuration_us = [
    phone_model_key,
    phone_chosen,
    operating_system,
    dimensions_us[:-1],
    weight_us.group(),
    touchscreen,
    screen_size,
    resolution,
    ppi,
    display_type,
    camera[:-2],
    video_recording,
    flash_type,
    front_camera,
    internal_storage[:-1],
    no_of_cores,
    processor,
    processor_speed,
    memory_card,
    sim_card,
    ram[:-1],
    positioning,
    radio,
    internet,
    wifi,
    bluetooth,
    hotspot,
    other,
    f"{battery.group()} mAh",
    "",
    "",
    "Yes",
]

# --------------------------------- Attribute Model Handset Data-------------------------------------------------------#

attribute_model_handset = [
    phone_chosen,
    phone_chosen.split(" ")[0],
    os,
    "touchscreen",
    "",
    float(dimensions_uk.split(" ")[0]),
    float(dimensions_uk.split(" ")[2]),
    float(screen_size[:-1]),
    int(ppi[:-4]),
    float(camera.split(" ")[1]),
    1,
    float(front_camera[:-2]),
    video_recording_attribute,
    release_quarter,
    int(release_year.group()),
    ""
]

# --------------------------------- Attribute Model Advanced Handset Data----------------------------------------------#

attribute_model_handset_advanced = [
    phone_chosen,
    water_resistance,
    "",
    "",
    "",
    "",
    "",
    "",
    wireless_charging,
    nfc,
    "",
    "",
    "",
    "",
    "",
    "",
    front_flash,
    ois,
    "",
    pixel_size,
    dual_camera,
    display_type,
    "",
    five_g
]


# --------------------------------- Complete config list -------------------------------------------------------#

complete_config = [device_configuration_uk, device_configuration_us,
                   attribute_model_handset, attribute_model_handset_advanced]

# --------------------------------- Add data to CSV -------------------------------------------------------#

with open("handset_data.csv", "w") as document:
    write = csv.writer(document)
    write.writerow(headers)
    write.writerows(complete_config)


# ----------------------------------------- Leap 1 Vectors ----------------------------------------------------------#

headers_leap1_vectors = [
    "phone",
    "OS",
    "small_is_best",
    "",
    "the_bigger_the_better",
    "",
    "take_pictures_and_videos",
    "",
    "watch_tv_and_films",
    "",
    "apps",
    "",
    "listen_to_music",
    "",
    "browsing_and_emails",
    "",
    "Default 1 ",
    "",
    "great_design",
    "",
    "Default 2"
]

# ----------------------------------------- Leap 2 Vectors ----------------------------------------------------------#

headers_leap2_vectors = [
    "Vector name",
    "Key Features",
    "Release date",
    "Level",
    "Camera quality",
    "Battery life",
    "Screen quality",
    "Screen size",
    "Screen quality & size",
    "Water resistance",
]

leap2_vectors = [
    phone_chosen,
    "",
    release_year,
    f"<strong> {camera} </strong> with",
    "Up to <strong> (HOURS HERE) hours </strong> talk time",
    f"{screen_size[:-1]}-inch <strong> {display_type} ADD EXTRA HERE </strong> display",
    f"Large <strong> {screen_size[:-1]}-inch </strong> {display_type} ADD EXTRA HERE display",
    f"Larger <strong> {screen_size[:-1]}-inch {display_type}</strong> ADD EXTRA HERE display",
    f"<strong> {water_resistance} </strong> water and dust resistant",
    five_g_vector,
]

with open("leap2_vectors.csv", "w") as document:
    write = csv.writer(document)
    write.writerow(headers_leap2_vectors)
    write.writerow(leap2_vectors)
