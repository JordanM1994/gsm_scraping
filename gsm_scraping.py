import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

phone_chosen = input("What phone are you looking for? ")
phone_chosen_amended = phone_chosen.replace(" ", "_").lower()
print(phone_chosen_amended)

url = "https://www.gsmarena.com/"

chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# -------------------------------------- Finding device page -----------------------------------------------#
driver.get(url)
time.sleep(2)

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
# ---------------------------------------UK-------------------------------------------------------------#
operating_system = driver.find_element(by=By.XPATH,
                                       value='//*[@id="specs-list"]/table[5]/tbody/tr[1]/td[2]').text.split(",")[0]
dimensions = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[1]/td[2]').text.split("(")[0]
weight = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[3]/tbody/tr[2]/td[2]').text.split("(")[0]
touchscreen = "Yes"
screen_size = driver.find_element(by=By.XPATH,
                                  value='//*[@id="specs-list"]/table[4]/tbody/tr[2]/td[2]').text.replace(" inches",'"').split(",")[0]

if "," in driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text:
    resolution = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text.split(",")[0]
else:
    resolution = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text.split(" (")[0]


display_type = driver.find_element(by=By.XPATH,
                                   value='//*[@id="specs-list"]/table[4]/tbody/tr[1]/td[2]').text.split(",")[0]
ppi = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[4]/tbody/tr[3]/td[2]').text.split("~")[1].replace(" density)",'')
camera = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[1]/td[1]/a').text
cameras = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[1]/td[2]').text.split("\n")
for n in cameras:
    split = n.split(",")
    camera += f" {split[0]} +"

video_recording = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[3]/td[2]').text.split(",")[0]
flash_type = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[7]/tbody/tr[2]/td[2]').text.split(",")[0]


if driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[1]/a').text == "Single":
    front_camera = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[2]').text.split(",")[0]
else:
    front_camera = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[8]/tbody/tr[1]/td[1]/a').text
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


no_of_cores = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[3]/td[2]').text.split("(")[0]
processor = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[2]/td[2]').text.split("(")[0]
processor_speed = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[5]/tbody/tr[3]/td[2]').text.split("(")[1].split(")")[0]
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
battery = driver.find_element(by=By.XPATH, value='//*[@id="specs-list"]/table[12]/tbody/tr[1]/td[2]').text.split(",")[0]



# ---------------------------------------US-------------------------------------------------------------#

print(operating_system)
print(dimensions)
print(weight)
print(touchscreen)
print(screen_size)
print(resolution)
print(display_type)
print(ppi)
print(camera[:-2])
print(video_recording)
print(flash_type)
print(front_camera[:-2])
print(internal_storage[:-1])
print(no_of_cores)
print(processor)
print(processor_speed)
print(memory_card)
print(sim_card)
print(ram[:-1])
print(positioning)
print(radio)
print(internet)
print(wifi)
print(bluetooth)
print(hotspot)
print(other)
print(battery)