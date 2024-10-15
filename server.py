from flask import Flask, jsonify, current_app, request
import json
#json is like a dictionary
#
app= Flask(__name__)

@app.route("/")
def html():
    return current_app.send_static_file("index.html")
#put the @ thing and the function you want next to each other 
@app.route("/players")
def hello():
    name_query = request.args.get("name") # query from the website url #different from the normal (url) requests
    age_query= request.args.get("age")
    #checks input of query if user inputs a "name"
    #if the "name" is not there the variable will be empty
    print(name_query)

    # gives you joel, if you put /players$name=joel
    
    
    with open("data/player_stats.json") as file: # Opens json file
        dc=json.load(file) # Loads the string into an array 
        #of dictionaries (because the file is technically just a long string)
        file.close()
        if name_query: # If the user typed in a name query
            for player in dc: # Go through each player dictionary
                # If the player's name starts with the name_query
                # Converts all letters to lowercase to prevent user error
                # e.g. TyrESe != tyrese, but TyrEse.lower() --> tyrese
                if player["Player"].lower().startswith(name_query.lower()):
                    return player # Return their dictionary
        elif age_query:
            pos_players=[]
            for player in dc:
                if player["Age"] == age_query:
                    pos_players.append(player)

            return pos_players
                
                        
app.run(host="0.0.0.0")#local host– my computer/ local ip, only computer itself can access local ip
