import requests
import re
import sys


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
	searchString="<{}>([a-zA-Z0-9\.\ \-]+)</{}>".format(fieldID,fieldID)
	m=re.search(searchString,bsmx)
	if m:
	    return(m.group(1))
	else:
		return("")

recipe_number=5080296
bsmx=getBSMX(recipe_number)
recipeName=getRecipeField("F_R_NAME",bsmx)


OG=getRecipeField("F_R_OG_MEASURED",bsmx)
FG=getRecipeField("F_R_FG_MEASURED",bsmx)
ABV=round((float(OG) - float(FG)) * 131.25,1)
brewDate=getRecipeField("F_R_DATE",bsmx)
beerStyle=getRecipeField("F_S_NAME",bsmx)

print(recipeName)
print("OG: {}".format(OG))
print("FG: {}".format(FG))
print("ABV: {}%".format(ABV))
print("Brew date: {}".format(brewDate))
print("Beerstyle: {}".format(beerStyle))

