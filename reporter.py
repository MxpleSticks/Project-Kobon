import json
import discord_webhook as dw

def sendResults(webhookURL, topResults, k, goalText):
    if(webhookURL == ""):
        return
    
    contentText = "Project Kobon Results\n"
    contentText += "Lines: " + str(k) + " Goal: " + goalText + "\n"
    contentText += "Top Scores:\n"
    
    for i in topResults:
        score = i[0]
        contentText += "Score: " + str(score) + " triangles\n"
    
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