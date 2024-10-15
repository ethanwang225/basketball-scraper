from bs4 import BeautifulSoup
import requests

url="https://basketball.realgm.com/international/league/12/French-Jeep-Elite/stats/2023/Averages/Qualified/All/points/All/desc/1/Regular_Season"
page= requests.get(url)
soup=BeautifulSoup(page.text, "html.parser")
csv=open("data/french_stats.csv", "w", encoding="utf-8")

all_player_stats=[]
all_players=soup.find_all("tr")
for player in all_players:
    player_statistics=[]
    stats= player.find_all("td")


    for i in range(len(stats)):
        stat= stats[i].text
        if i==1:
             stat=stat.replace(",", "")
        stat+=","
        print(stats[i])
        
        csv.write(stat.rstrip('\n'))
        player_statistics.append(stats[i].text)
    csv.write('\n')

    

    #remove the number of 
    if player_statistics:
            player_statistics.pop(0)
    all_player_stats.append(player_statistics)

all_player_stats.pop(0)
print(all_player_stats)
csv.close()

