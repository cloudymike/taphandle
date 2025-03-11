import sys
import re
import urequests as requests

import wlan
import network

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

        except:
            print(f"Error fetching page {page_number}")
            break
        
        page_number += 1
    return(recipelist)


if __name__ == "__main__":
    mynetwork = wlan.do_connect('wlan_test')


    recipelist=fetch_recipe_numbers()
    print(recipelist)

    print("All done!")
