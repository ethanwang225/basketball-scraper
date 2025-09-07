from nba_api.stats.endpoints import playercareerstats, teamyearbyyearstats
from nba_api.stats.library.parameters import SeasonTypeAllStar, PerModeSimple, LeagueID
from flask import Flask, jsonify, current_app, request
from nba_api.stats.static import players, teams
import requests
import os
import certifi
from dotenv import load_dotenv
import ssl
import time

# Load env variables
load_dotenv()
# proxy_username=os.getenv("PROXY_USERNAME")
# proxy_password=os.getenv("PROXY_PASSWORD")

# address = 'dc.oxylabs.io:8000'
max_query_retries = 5

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
    import requests
    from dotenv import load_dotenv
    import os
    import certifi

    # Replace with your proxy user credentials.
    load_dotenv()
    username=os.getenv("PROXY_USERNAME")
    password=os.getenv("PROXY_PASSWORD")

    # Port `8000` rotates IPs from your proxy list.
    address = 'dc.oxylabs.io:8000'

    proxies = {
        'http': f'https://user-{username}:{password}@{address}'
    }

    response = requests.get('https://ip.oxylabs.io/location', proxies=proxies, verify=certifi.where())
    return jsonify({"message":"hello world", "ssl": ssl.OPENSSL_VERSION, "response": response.text})
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

    url = f"https://d6e444641b34.ngrok-free.app/players?name={name_query}&team={team_query}&season={season_query}&seasontype={seasonTquery}&leaguetype={leagueTquery}&pergame={perGameQuery}"

    r = requests.get(url)
    print(r.json())
    return r.json()



                
if __name__=="__main__" :
    app.run(host="0.0.0.0", debug=True)#local host– my computer/ local ip, only computer itself can access local ip
