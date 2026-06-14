import json
import discord_webhook as dw
from Theory.theory import tamuraUpperBound

def sendResults(webhookURL, topResults, k, goalText):
    if(webhookURL == ""):
        return
    
    ceiling = tamuraUpperBound(k)

    contentText = "@everyone\n"
    contentText += "**△ PROJECT KOBON RESULTS △**\n\n"
    contentText += "[△ PARAMETERS ]\n"
    contentText += "|- Upper Bound :  " + str(ceiling) + " triangles\n"
    contentText += "|- Lines :  " + str(k) + "\n"
    contentText += "|- Goal :  " + goalText + " Triangles\n\n"
    contentText += "[△ BEST RESULTS ]\n"
    
    rank = 1

    for i in topResults:
        contentText += "|#" + str(rank) + "  " + str(i[0]) + " triangles\n"
        rank += 1
    
    saveData = []

    for i in topResults:
        arrangement = i[1]
        linesList = []

        for j in arrangement:
            linesList.append({"angle": j.angle, "offset": j.offset})
    
        saveData.append({"score": i[0], "lines": linesList})
    
    jsonString = json.dumps(saveData, indent=4)
    fileBytes = jsonString.encode("utf-8")

    webHook = dw.DiscordWebhook(url=webhookURL, content=contentText)
    webHook.add_file(file=fileBytes, filename="results.json")
    webHook.execute()