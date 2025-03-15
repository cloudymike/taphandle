import requests
import re
import sys


def getBSMX(recipe_number):
	base_url="https://beersmithrecipes.com/download.php?id="
	url = f"{base_url}{str(recipe_number)}"
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

def getIBUfindall(bsmx):
	fieldID="F_H_IBU_CONTRIB"
	searchString="<{}>([a-zA-Z0-9\.\ \-]+)</{}>".format(fieldID,fieldID)
	m=re.findall(searchString,bsmx)
	print(m)
	ibu=0
	for x in m:
		ibu = ibu+float(x)
	ibu=round(ibu,1)
	return(ibu)

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
	ibu=round(ibu,1)
	return(ibu)


recipe_number=5080296

#recipelist=[['4886853', '332 NEIPA Phantasm Cosmic'], ['5020079', '341 Jamils Lefty Blond'], ['4936551', '347 Dennyish'], ['5041259', '348 Kolsch Mt Hood'], ['5080296', '349 NEIPA'], ['5085634', '350 Saison wo Raison'], ['5125883', '351 Maltose falcons 50th anniversary IPA'], ['5131069', '352 Deschutes Black Butte Porter AHA']]
#recipelist=[['5131069', '352 Deschutes Black Butte Porter AHA']]
recipelist=[['5080296', '349 NEIPA']]
for recipe in recipelist:
	recipe_number=recipe[0]
	bsmx=getBSMX(recipe_number)
	recipeName=getRecipeField("F_R_NAME",bsmx)


	OG=getRecipeField("F_R_OG_MEASURED",bsmx)
	og=round(float(OG),3)
	FG=getRecipeField("F_R_FG_MEASURED",bsmx)
	ABV=round((float(OG) - float(FG)) * 131.25,1)
	brewDate=getRecipeField("F_R_DATE",bsmx)
	beerStyle=getRecipeField("F_S_NAME",bsmx)
	IBU=getIBU(bsmx)

	print(recipeName)
	print("OG: {0:.3f}".format(og))
	print("FG: {}".format(FG[:5]))
	print("ABV: {}%".format(ABV))
	print("IBU: {}".format(IBU))
	print("Brew date: {}".format(brewDate))
	print("Beerstyle: {}".format(beerStyle))

	



