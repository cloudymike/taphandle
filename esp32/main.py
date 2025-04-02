import sys
import re
import urequests as requests

import wlan
import network

from machine import Pin
from time import sleep, sleep_ms
import textout

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

def getIBU(bsmx):
	ibu=0
	pattern="<F_H_IBU_CONTRIB>"
	p=re.compile(pattern)
	s = p.split( bsmx )
	for id in s:
		m=re.match("([0-9\.]+)</F_H_IBU_CONTRIB>",id)
		if m:
			print(m.group(1))
			ibu = ibu+float(m.group(1))
	return(ibu)


# Scoll one item in list for each time button pressed
# When no more scrolling for 10s return recipe item.
def scroll(tout, scrollList):
    for current in range(len(scrollList)+1):
        element=scrollList[current]
        recipeName=element[1]
        tout.terminalline(recipeName)
        if not buttonPressed():
            break
    return(scrollList[current])




# ESP32 Pin assignment
sw = Pin(13, Pin.IN, Pin.PULL_UP) 
txtout = textout.textout()

txtout.text('Starting...')

mynetwork = wlan.do_connect('wlan_test')

txtout.text('Fetching...')

recipelist=fetch_recipe_numbers()
print(recipelist)
txtout.clear()
txtout.leftline('Push button', 1)
txtout.leftline('to scroll recipies', 2)
txtout.leftline('Stop when recipe', 3)
txtout.leftline('is found and', 4)
txtout.leftline('on top of list', 5)
txtout.show()
buttonPressed()
txtout.clear()
recipe=scroll(txtout, recipelist)

bsmx=getBSMX(recipe[0])
OG=getRecipeField("F_R_OG_MEASURED",bsmx)
FG=getRecipeField("F_R_FG_MEASURED",bsmx)
ABV=round((float(OG) - float(FG)) * 131.25,1)
brewDate=getRecipeField("F_R_DATE",bsmx)
beerStyle=getRecipeField("F_S_NAME",bsmx)
IBU=getIBU(bsmx)

txtout.clear()
txtout.leftline(recipe[1],0)
txtout.leftline(beerStyle,1)
txtout.leftline(brewDate,2)
txtout.leftline("ABV: {}%".format(ABV),3)
txtout.leftline("IBU: {}".format(round(IBU)),4)
txtout.leftline("OG: {}".format(OG[:5]),5)
txtout.show()
print("All done!")
