import json
file=open("data/player_stats.csv", "r")
dc=[]
output=open("data/player_stats.json", "w")

line=file.readline()#takes a single line in the file
keys=line.split(",")

while True:
    player={}
    line=file.readline()
    if line:
        vars= line.split(",") # seperates the line into a list
        for i in range(1,len(keys)-3):
            player[keys[i]]= vars[i]
            
        dc.append(player)
    else: 
        break

print(dc)
output.write(json.dumps(dc))
output.close()
file.close()