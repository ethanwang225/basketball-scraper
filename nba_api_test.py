from nba_api.stats.endpoints import playercareerstats
from flask import Flask, jsonify, current_app, request
import json
from nba_api.stats.static import players, teams

import csv

# Nikola Jokić



#json is like a dictionary
#
app= Flask(__name__)

@app.route("/")
def html():
    return current_app.send_static_file("index.html")
#put the @ thing and the function you want next to each other
# https://basketball-scraper.onrender.com/players
# https://basketball-scraper.onrender.com/hello?name="What we typed in wix"&

@app.route("/hello", methods=['GET'])
def hello():
    name_query = request.args.get("name")
    team_query= request.args.get("team")
    season_query=request.args.get("season")
    return jsonify({"message":"hello world"+name_query+team_query+season_query}) 
@app.route("/players", methods=['GET'])
def handlequery():
    #checks input of query if user inputs a "name"
    #if the "name" is not there the variable will be empty
    name_query = request.args.get("name") # query from the website url #different from the normal (url) requests
    team_query= request.args.get("team")
    reb_query=request.args.get("reb")
    pts_query=request.args.get("pts")
    ast_query=request.args.get("ast")
    stl_query=request.args.get("stl")
    season_query=request.args.get("season")
    

    #player_name=players.get_players()
    

    player_name=players.find_players_by_full_name(name_query)



    #team_name=teams.find_teams_by_full_name(team_query)
    #result is a list of all the player that matches the query 
    #print(result)
    

    if player_name:
        players_json={}
        

        print(len(player_name))
        player_ids=[]
        for player in player_name:
            player_ids.append(player["id"])
        #print(player_ids)
        temp = playercareerstats.PlayerCareerStats(player_id=player_ids[0]) 
        response =temp.get_dict()
        headers= response["resultSets"][0]["headers"] # list
        players_json["headers"]=headers # players_json = {"headers": [list of stat names (PTS, REB, etc.)]}


        csvfile = open('file.csv', 'w')
        for header in headers:
            csvfile.write(header + ",")
        csvfile.write('PTS/GAME')
        csvfile.write('\n')


        players_json["players"]=[]
        for id in player_ids:
            csvfile = open('file.csv', 'a')
            career = playercareerstats.PlayerCareerStats(player_id=id) 


        
            response =career.get_dict()
        
            
            rows=response["resultSets"][0]["rowSet"]
            players_json["players"].append(rows)

            if season_query:
                newrows=[]
                for i in range(len(rows)):
                    if rows[i][1].startswith(str(season_query)):
                        newrows.append(rows[i])
                    else:
                        pass

                for row in newrows:
                    for data in row:
                        csvfile.write(str(data) +",")
                    csvfile.write(str(round(row[26]/row[6],2)))
                    csvfile.write("\n")
                csvfile.close()
            else:    
                for row in rows:
                    for data in row:
                        csvfile.write(str(data) +",")
                    csvfile.write(str(round(row[26]/row[6],2)))
                    csvfile.write("\n")
                csvfile.close()

    # elif team_name:
    #     pass
    csvfile.close()
    return jsonify(players_json)


#for filtering stats: do response=career.get_dict()
#in rowSets look at 2nd element or whatever your filtering and then check if it matches 
#rowsets[i][thingyour trying to filter].startswith(year_query)
#once u get it you can add it to csv file

    
                
                        
app.run(host="0.0.0.0")#local host– my computer/ local ip, only computer itself can access local ip
