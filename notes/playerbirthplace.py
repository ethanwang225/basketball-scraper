from bs4 import BeautifulSoup
import re
import requests
import time
url="https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
page=requests.get(url)
#page.text is the entire html
#robots.txt at the end of a website to look at how much requests you can do
# Extract data
soup=BeautifulSoup(page.text, "html.parser")
#turns page.text into a soup object

condensed= soup.find("tbody")
player_urls=condensed.find_all("tr")
player_born=[]
for player in player_urls:

    player_info=[]
    try:
        href_line= player.find("a")
        player_info.append(href_line.text)
        if href_line:
            href=href_line.get("href")
            individual_page="https://www.basketball-reference.com"+ href
            #wait 10 seconds until you make another request to not get banned
            time.sleep()
            individual_html=requests.get(individual_page)
            indi_soup=BeautifulSoup(individual_html.text, "html.parser")
            FAQ_player= indi_soup.find("div", {"id": "div_faq"})
            
            born_in=FAQ_player.find("p", text=re.compile("born in"))

            

            #-1 gives the end of the list (exlusive of the period)
            place= born_in.text[born_in.text.index(", ")+2: -1]

            print(place)
            player_born.append(place)
    except:
        print("player did not have born in, skipping")
           


print(player_born)
      