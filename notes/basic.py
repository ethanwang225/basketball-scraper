import requests

# hello= "hello world"
# substring= hello[:5]
# #same as hello[0:5]
# #[5:] starts at index 5 and goes to the end (in this case world)
# print(substring)
# #start:end [inclusive:exclusive]
# print(hello.index("world"))


#Scraping
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

url= "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
page= requests.get(url)

#doing some condensing
startplayer= page.text.index("Player Per Game Table")
small= page.text[startplayer:]
endplayer= small.index("placeholder")
small= page.text[startplayer:endplayer]
# print(small)

#searching for player name
player_idxs = list(find_all(page.text, "\"player\""))
all_players = []

for idx in player_idxs:
    try:
        player=[]
        #we need to make it so that the player is the first one we see
        #condenses into the whole row as tr means row in html
        snippet= page.text[idx:]
        snippet=snippet[:snippet.index("</tr>")]
        # print(snippet)
        #get each stat
        #get name
        name_start= snippet.index(".html")+7
        name_end=snippet.index("</a>")
        name=snippet[name_start:name_end]
        player.append(name)
        print(player)

        stat_idxs=list(find_all(snippet, "data-stat=\""))
       
        for i in range(len(stat_idxs)):
            
            #isolate stat
            stat_snippet=snippet[stat_idxs[i]:]
            
            #fix beginning
            stat_snippet=stat_snippet[(stat_snippet.index(">")+1):]
            
            

            #fix end
            stat_snippet=stat_snippet[:stat_snippet.index("</td>")]
            print(stat_snippet)
            if i == 2: 
                # This is the index of the team stat, which has an <a> inside, so we have to deal with it in the else
                stat_snippet = stat_snippet[(stat_snippet.index(">")+1):stat_snippet.index("</a>")]
            player.append(stat_snippet)
            print(stat_snippet)
        
        all_players.append(player)
      

    except:
        continue
print(all_players)














# statindexs=list(find_all(small,"data-stat"))

# playersnba=list()


    
# for i in range(len(nameindexs)):
#         substring = small[nameindexs[i]: nameindexs[i] + 50]
#         endname = substring.find("</a>")
#         name = substring[27:endname]

#         player = list()
#         player.append(name)
    
#         if i + 1 < len(nameindexs):
#             playerstat = small[nameindexs[i]:nameindexs[i+1]]

#             for z in range(len(statindexs)): #playerstat is a condensed substring from one player to the other player
#                     if statindexs[z]>=nameindexs[i] and statindexs[z]<nameindexs[i+1]:
#                         start_stat = statindexs[z]
#                         end_stat = statindexs[z+1] if z+1 < len(statindexs) else len(playerstat)
                        
#                         stat_snippet = playerstat[start_stat:end_stat]
#                         player.append(stat_snippet)


               

                
                
                    
               
                
                
#         else:
#         # Handle the case where i+1 is out of bounds
#             playerstat = small[nameindexs[i]:]
#             for z in range(len(statindexs)): #playerstat is a condensed substring from one player to the other player
#                     start_stat = statindexs[z]
#                     end_stat = statindexs[z+1] if z+1 < len(statindexs) else len(playerstat)
                    
#                     stat_snippet = playerstat[start_stat - nameindexs[i]:end_stat - nameindexs[i]]
#                     player.append(stat_snippet)

#         playersnba.append(player)

# print(playersnba)