from nba_api.stats.endpoints import playercareerstats, teamyearbyyearstats
from nba_api.stats.library.parameters import SeasonTypeAllStar, PerModeSimple, LeagueID
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
    seasonTquery=request.args.get("seasontype")
    leagueTquery=request.args.get("leaguetype")
    perGameQuery=request.args.get("pergame")



    

    #player_name=players.get_players()
    

    

    
    #team_name=teams.find_teams_by_full_name(team_query)
    #result is a list of all the player that matches the query 
    #print(result)
    

    if name_query:
        player_name=players.find_players_by_full_name(name_query)
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

        

                # newrows=[]
                # for i in range(len(rows)):
                #     if rows[i][1].startswith(str(season_query)):
                #         newrows.append(rows[i])
                #     else:
                #         pass

                # for row in newrows:
                #     for data in row:
                #         csvfile.write(str(data) +",")
                #     csvfile.write(str(round(row[26]/row[6],2)))
                #     csvfile.write("\n")
                # csvfile.close()

            
            # else:    
            #     for row in rows:
            #         for data in row:
            #             csvfile.write(str(data) +",")
            #         csvfile.write(str(round(row[26]/row[6],2)))
            #         csvfile.write("\n")
            #     csvfile.close()
        
        if season_query and team_query:
            players_json["players"] = filter_by_seasonandteam(players_json["players"], season_query, team_query)
        elif season_query:
            players_json["players"] = filter_by_season(players_json["players"], season_query)
        elif team_query:
            players_json["players"]=filter_by_team(players_json["players"], team_query)

        
        csvfile.close() 
        return jsonify(players_json)


    elif team_query:
        team_info=teams.find_team_by_abbreviation(team_query)
        print(team_info)
        team_id=team_info['id']

        team_json={}
        #do this for everyone
        perGame=PerModeSimple.totals
        if perGameQuery=="pergame":
            perGame=PerModeSimple.per_game
        

        season_type=SeasonTypeAllStar.regular
        if seasonTquery=="playoffs":
            season_type=SeasonTypeAllStar.playoffs
        elif seasonTquery=="preseason":
            season_type=SeasonTypeAllStar.preseason

        league=LeagueID.nba
        if leagueTquery=="summer":
            league=LeagueID.summer_league
        elif leagueTquery=="gleague":
            league=LeagueID.g_league
        #TO DO: DO THE SAME THING FOR THE OTHER LEAGUES
        print(season_type)

        
        #print(player_ids)
        temp = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id, 
                                                       league_id=league, 
                                                       season_type_all_star=season_type, 
                                                       per_mode_simple= perGame ) 
        response =temp.get_dict()
        
        headers= response["resultSets"][0]["headers"] # list
        team_json["headers"]=headers 
        team_json["seasons"]=response["resultSets"][0]["rowSet"]
        
        
        if season_query:
            team_json["seasons"] = filter_by_teamseason(team_json["seasons"], season_query)    
        
        
        return jsonify(team_json)
    
    


#for filtering stats: do response=career.get_dict()
#in rowSets look at 2nd element or whatever your filtering and then check if it matches 
#rowsets[i][thingyour trying to filter].startswith(year_query)
#once u get it you can add it to csv file

# name_query
# get players with that name --> player_list
# player_list = filter_by_season(player_list)
# player_list = filter_by_team(player_list)
# player_list = filter_by_pts(player_list)
# player_list = filter_by_reb(player_list)
# player_json[""]

# return jsonify(player_json)

def filter_by_season(players: list, season: int):
    allplayers=[]
    for player in players:
        playerseason=[]
        for row in player:
            
            if row[1].startswith(season):
                playerseason.append(row)
        if playerseason:
            allplayers.append(playerseason)

    return allplayers

def filter_by_teamseason(team: list, year: int):
    A=[]
    
    for season in team:
        if season[3].startswith(year):
            A.append(season)
       


    return [A]

def filter_by_seasonandteam(players: list, year: int, team: str ):
   
    players= filter_by_season(players, year)
    
    players=filter_by_team(players, team)
       


    return players


def filter_by_team(players: list, team_name: str):
    allplayers=[]
    for player in players:
        playerseason=[]
        for season in player:
            
            if season[4].startswith(team_name):
                playerseason.append(season)
        if playerseason:
            allplayers.append(playerseason)
    return allplayers



                
if __name__=="__main__" :
    app.run(host="0.0.0.0", debug=True)#local host– my computer/ local ip, only computer itself can access local ip
