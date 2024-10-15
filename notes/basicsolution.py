import requests

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

# Request basketball stats page
page = requests.get("https://www.basketball-reference.com/leagues/NBA_2024_totals.html")

# Find all instances of "player" in the page HTML
player_idxs = list(find_all(page.text, "\"player\""))
# Pop the first player (we don't want the top bar)
player_idxs.pop(0)

all_players = []

# Traverse through every instance of "player"
for idx in player_idxs:
    # Wrap in try, except which will prevent program from stopping if errors occur
    try:
        # Create list that will store all player info
        player = []
        # Create a substring from "player" (this is so the
        # player we're looking at is the FIRST one we see)
        # And stop at the end of this player's stats
        snippet = page.text[idx:]
        snippet = snippet[:snippet.index("</tr>")]

        # Get each stat
        # Get name
        name_start = snippet.index(".html") + 7
        name_end = snippet.index("</a>")
        name = snippet[name_start:name_end]

        # Append name to player list
        player.append(name)

        # Use find_all function to find all instances of "data-stat=\""
        # This will get the rest of the stats
        # (We didn't do this for name because it was inside an <a></a>)
        stat_idxs = list(find_all(snippet, "data-stat=\""))

        for i in range(len(stat_idxs)):
            # Isolate stat
            stat_snippet = snippet[stat_idxs[i]:]
            # Fix beginning
            stat_snippet = stat_snippet[stat_snippet.index(">")+1:]
            # Fix end
            stat_snippet = stat_snippet[:stat_snippet.index("</td>")]
            if i == 2: # This is the index of the team stat, which has an <a> inside, so we have to deal with it in the else
                stat_snippet = stat_snippet[stat_snippet.index(">")+1:stat_snippet.index("</a>")]

            # Append this stat
            player.append(stat_snippet)
        
        # Finally, add to all_players list
        all_players.append(player)
    except:
        continue

for player in all_players:
    print(player)