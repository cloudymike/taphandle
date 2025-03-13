import sys
import re
import urequests as requests

import wlan
import network

from machine import Pin, I2C
import ssd1306
from time import sleep, sleep_ms

def extract_recipe_number(text: str) -> list:
    """
    Extracts all numbers following the viewrecipe pattern in the text.

    Args:
        text (str): Input text containing viewrecipe links.

    Returns:
        list: List of recipe numbers as strings.
    """
    recipelist=[]
    pattern = "href='https://beersmithrecipes\.com/viewrecipe/"
    p=re.compile(pattern)
    s = p.split( text )
    for id in s:
        m=re.match("(\d+)/[a-zA-Z0-9\-]+\'>([a-zA-Z0-9\-\ ]+)<",id)
        if m:
            print(m.group(0))
            print(m.group(1))
            print(m.group(2))
            recipelist.append([m.group(1),m.group(2)])
    return(recipelist)

def fetch_recipe_numbers():
    base_url = "https://beersmithrecipes.com/listrecipes/5399/"
    page_number = 0

    recipelist=[]

    while True:
        url = f"{base_url}{page_number}"
        try:
            response = requests.get(url)
        except:
            print(f"Error fetching page {page_number}")
            break
        
        # Check if the request was successful and content is not empty
        if response.status_code != 200 or not response.content.strip():
            print(f"No data found at page {page_number}. Exiting.")
            break
        
        # Extract names using regex for viewrecipe links
        matches = extract_recipe_number(response.text)
        if matches:
            recipelist.extend(matches)
        else:
            print(f"No recipes found on page {page_number}.")
            return(recipelist)

        
        page_number += 1
    return(recipelist)


def displayList(oled,scrollList):
    oled.fill(0)
    i=1
    for recipe in scrollList:
        oled.text(recipe[1], 0, (len(scrollList)-i)*10)
        i=i+1
    oled.show()

def makeList():
    scrollList=[]
    for number in range(15):
        recipe=[str(number),'Hello, World {}'.format(number)]
        scrollList.append(recipe)
    return(scrollList)

def buttonPressed():
    waittime=0
    while not sw.value():
        sleep_ms(10)
    while waittime<100:
        if sw.value():
            waittime=waittime+1
        else:
            return(True)
        sleep(0.1)
    return(False)


def getBSMX(recipe_number):
	base_url="https://beersmithrecipes.com/download.php?id="
	url = f"{base_url}{str(recipe_number)}"
	print(url)
	try:
	    response = requests.get(url)
	    
	    # Check if the request was successful and content is not empty
	    if response.status_code != 200 or not response.content.strip():
	        print(f"No data found for recipe {recipe_number}. Exiting.")
	        bsmx=None
	    else:
	        bsmx=response.text

	except requests.RequestException as e:
	    print(f"Error fetching page {page_number}: {e}")
	    bsmx=None

	return(bsmx)

def getRecipeField(fieldID, bsmx):
	searchString="<{}>([a-zA-Z0-9\.\-\ ]+)</{}>".format(fieldID,fieldID)
	m=re.search(searchString,bsmx)
	if m:
	    return(m.group(1))
	else:
		return("")

# Scoll one item in list for each time button pressed
# When no more scrolling for 10s return recipe item.
def scroll(oled,scrollList):
    if not len(scrollList):
        return([])
    for current in range(1,len(scrollList)+1,1):
        displayList(oled,scrollList[0:current])
        if not buttonPressed():
            break
    return(scrollList[current-1])



# ESP32 Pin assignment
sw = Pin(13, Pin.IN, Pin.PULL_UP) 

i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

# Reset OLED
oledReset=Pin(16, Pin.OUT)
oledReset.value(0)
sleep_ms(500)
oledReset.value(1)

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text('Starting...', 10, 30)
oled.show()

mynetwork = wlan.do_connect('wlan_test')

oled.fill(0)
oled.text('Fetching', 0, 30)
oled.text('  recipies...', 0, 40)
oled.show()

recipelist=fetch_recipe_numbers()
print(recipelist)

oled.fill(0)
oled.text('Push button', 0, 10)
oled.text('to scroll recipies', 0, 20)
oled.text('Stop when recipe', 0, 30)
oled.text('is found and', 0, 40)
oled.text('on top of list', 0, 50)
oled.show()
buttonPressed()
recipe=scroll(oled,recipelist)

bsmx=getBSMX(recipe[0])
OG=getRecipeField("F_R_OG_MEASURED",bsmx)
FG=getRecipeField("F_R_FG_MEASURED",bsmx)
ABV=round((float(OG) - float(FG)) * 131.25,1)
brewDate=getRecipeField("F_R_DATE",bsmx)
beerStyle=getRecipeField("F_S_NAME",bsmx)

oled.fill(0)
oled.text(recipe[1],0,0)
oled.text(beerStyle,0,10)
oled.text(brewDate,0,20)
oled.text("ABV: {}%".format(ABV),0,30)
oled.text('The end!', 60, 50)
oled.show()

print("All done!")
