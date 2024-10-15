from bs4 import BeautifulSoup
import requests
url="https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
page=requests.get(url)
#page.text is the entire html

# Extract data
all_players_stats=[]
soup=BeautifulSoup(page.text, "html.parser")
#turns page.text into a soup object
print(soup)

all_players=soup.find_all("tr")
print(all_players)
for player in all_players:
    # print(player.text)
    #.text here removes the html tags

    player_stats = []
    stats = player.find_all("td")
    for stat in stats:
        
        # type_of_stat = stat["data-stat"]
        # string = type_of_stat + " : " + stat.text
        player_stats.append(stat.text)
    all_players_stats.append(player_stats)

# Print data
for player in all_players_stats:
    print(player)

