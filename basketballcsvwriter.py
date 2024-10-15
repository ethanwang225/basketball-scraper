from bs4 import BeautifulSoup
import requests
import time
import re
#make file
csv=open("data/player_stats.csv", "w", encoding="utf-8")
#open("w") means write which overwites everything–if you write something in w mode, its just going to delete everything when you write it
# open("a") means append, which will add it to everything you already have

url="https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
page=requests.get(url)
#page.text is the entire html

# Extract data
all_players_stats=[]
soup=BeautifulSoup(page.text, "html.parser")
#turns page.text into a soup object


all_players=soup.find_all("tr")
title_text = all_players[0]
title_text.find_all("th")
titles = []
counter = 0
for title in title_text:
    if counter % 2 != 0: # every odd one
        titles.append(title.text)
    counter += 1
titles.append("birthplace")

# Write to file
# Titles
awards_index=0
for i in range(len(titles)):
    text = titles[i] + "," # Add a comma in between data so they're in different boxes
    if titles[i]=="Awards":
        awards_index=i
    csv.write(text.rstrip('\n')) # Remove the new line so its on the same line
csv.close()

rank = 0 # This adds the Rk so that the titles and stats are aligned
for player in all_players:
    # print(player.text)
    #.text here removes the html tags
    csv=open("data/player_stats.csv", "a", encoding="utf-8")

    player_stats = []
    birthplace=""
    try:
        href_line= player.find("a")
        if href_line:
            href=href_line.get("href")
            individual_page="https://www.basketball-reference.com"+ href
            #wait 3 seconds until you make another request to not get banned
            time.sleep(3.1)
            individual_html=requests.get(individual_page)
            indi_soup=BeautifulSoup(individual_html.text, "html.parser")
            FAQ_player= indi_soup.find("div", {"id": "div_faq"})
            
            born_in=FAQ_player.find("p", text=re.compile("born in"))

            

            #-1 gives the end of the list (exlusive of the period)
            place= born_in.text[born_in.text.index(", ")+2: -1]

            birthplace=place

    except:
        print("player did not have born in, skipping")
    stats = player.find_all("td")
    text = str(rank) + "," # Add comma
    csv.write(text.rstrip('\n'))
    for i in range(len(stats)):
        
        stat_text = stats[i].text 
        if i>=awards_index-1:
            stat_text=stat_text.replace(",", " ")
        stat_text+=","
        csv.write(stat_text.rstrip('\n'))# whenever you write to a file in python it automatically 
        #writes the next thing to a new line, we want this to be on the same line
        #"x"->"x\n"
            
        
        # type_of_stat = stat["data-stat"]
        # string = type_of_stat + " : " + stat.text
    csv.write( birthplace+ "," ) 
    csv.write("\n")
    csv.close()
    print("added " + stats[0].text)
    rank+=1



   