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

url = "https://www.gsmarena.com/"

chrome_driver_path = "/Users/jordanmcleod/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# -------------------------------------- Finding device page -----------------------------------------------#
driver.get(url)
time.sleep(3)

agree = driver.find_element(by=By.XPATH, value='//*[@id="unic-b"]/div/div/div/div[3]/div[1]/button[2]')
agree.click()

time.sleep(2)

search = driver.find_element(by=By.XPATH, value='//*[@id="topsearch-text"]')
search.send_keys(phone_chosen)
search.send_keys(Keys.ENTER)

time.sleep(3)
phone_link = driver.find_element(by=By.CSS_SELECTOR, value=f"a[href*={phone_chosen_amended}]")
phone_link.click()

time.sleep(3)

# ------------------------ All config for devices ---------------------------------------------------#
release_year_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[2]/tbody/tr[2]/td[2]').text
release_year = re.search('[0-9][0-9][0-9][0-9]', release_year_data)

release_quarter_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[2]/tbody/tr[2]/td[2]').text.lower()

if "january" or "february" or "march" in release_quarter_data:
    release_quarter = 1
elif "april" or "may" or "june" in release_quarter_data:
    release_quarter = 2
elif "july" or "august" or "september" in release_quarter_data:
    release_quarter = 3
elif "october" or "november" or "december" in release_quarter_data:
    release_quarter = 4

try: operating_system = driver.find_element(by=By.XPATH,
                                       value='//*[@id="specs-list"]/table[5]/tbody/tr[1]/td[2]').text.split(",")[0]
except NoSuchElementException:
    operating_system = ""

if "Android" in driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[1]/td[2]').text:
    os = "android"
elif "iOS" in driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[1]/td[2]').text:
    os = "apple_ios"
else:
    os = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[1]/td[2]').text.split(",")[0]

dimensions_uk = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[1]/td[2]').text.split("(")[0]
weight_uk = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[2]/td[2]').text.split("(")[0]

dimensions_us = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[1]/td[2]').text.split("(")[1]

weight_us_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[2]/td[2]').text
weight_us = re.search('[0-9][.][0-9][0-9][ ][o][z]', weight_us_data)

touchscreen = "Yes"
screen_size = driver.find_element(by=By.XPATH,
                                  value='//*[@id="specs-list"]/table[4]/tbody/tr[2]/td[2]').text.replace(" inches", '"').split(",")[0]

if "," in driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text:
    resolution = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text.split(",")[0]
else:
    resolution = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text.split(" (")[0]


display_type = driver.find_element(by=By.XPATH,
                                   value='//*[@id="specs-list"]/table[4]/tbody/tr[1]/td[2]').text.split(",")[0]
ppi = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text.split("~")[1].replace(" density)", '')
camera = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[1]/td[1]/a').text
cameras = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[1]/td[2]').text.split("\n")
for n in cameras:
    split = n.split(",")
    camera += f" {split[0]} +"

video_recording = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[3]/td[2]').text.split(",")[0]
video_recording_attribute_data = video_recording.split('@')[0].lower()
if "k" in video_recording_attribute_data:
    video_recording_attribute = int(video_recording_attribute_data[0])*1000
else:
    video_recording_attribute = int(video_recording_attribute_data.split("p")[0])

flash_type = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[2]/td[2]').text.split(",")[0]


if driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[1]/a').text == "Single":
    front_camera = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[2]').text.split(",")[0]
else:
    front_camera = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[1]/a').text[:-2]
    front_cameras = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[2]').text.split("\n")
    for cam in front_cameras:
        split = cam.split(",")
        front_camera += f" {split[0]} +"

internal_storage = ""

internal_storage_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[6]/tbody/tr[2]/td[2]').text.split(",")
for storage in internal_storage_data:
    if storage[0] == " ":
        split = storage[1:].split(" ")[0]
    else:
        split = storage.split(" ")[0]
    if split in internal_storage:
        pass
    else:
        internal_storage += f"{split}/"


try:
    no_of_cores = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[3]/td[2]').text.split("(")[0]
except NoSuchElementException:
    no_of_cores = ""

processor = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[2]/td[2]').text.split("(")[0]

try:
    processor_speed_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[3]/td[2]').text.split("\n")
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

memory_card = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[6]/tbody/tr[1]/td[2]').text
sim_card = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[4]/td[2]').text
if "Nano" in sim_card:
    sim_card = "Nano"
elif "micro" in sim_card:
    sim_card = "Micro"
else:
    sim_card = "Standard"

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


positioning = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[3]/td[2]').text.split("with ")[1]
if "Unspecified" in driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[5]/td[2]').text:
    radio = "No"
else:
    radio = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[5]/td[2]').text
internet = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[1]/td[2]').text
if "Wi-Fi" in internet:
    internet = "Yes"
else:
    internet ="No"

wifi = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[1]/td[2]').text
if "Wi-Fi" in wifi:
    wifi = "Yes"
else:
    wifi ="No"

bluetooth = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[2]/td[2]').text
if bluetooth == "No":
    bluetooth = "No"
else:
    bluetooth ="Yes"

hotspot = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[1]/td[2]').text
if "hotspot" in hotspot:
    hotspot = "Yes"
else:
    hotspot ="No"
other = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[10]/tbody/tr[4]/td[2]').text

battery_data = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[12]/tbody/tr[1]/td[2]').text
battery = re.search(r'\b\d+\b', battery_data)

headers = [
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
]

device_configuration_uk = [
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
]

device_configuration_us = [
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
]

attribute_model_handset = [
    phone_chosen,
    phone_chosen.split(" ")[0],
    os.lower(),
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

complete_config = [device_configuration_uk, device_configuration_us, attribute_model_handset]

with open("handset_data.csv", "w") as document:
    write = csv.writer(document)
    write.writerow(headers)
    write.writerows(complete_config)


