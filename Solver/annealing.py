import numpy as np
import random
import math

from Solver.geometry import countTriangles
from Solver.state import createRandomState, nudge
from Theory.theory import tamuraUpperBound

startTemperature = 10.0
coolingRate = 0.995

def updateResults(topResults, arrangement, score):
    for i in topResults:
        if(i[0] == score):
            return topResults
    
    topResults.append([score, arrangement])
    topResults.sort(reverse=True)
    
    if(len(topResults) > 3):
        topResults.pop()
    
    return topResults

def runAnnealing(k, iters, restarts, goalText):
    topResults = []

    for i in range(restarts):
        currentState = createRandomState(k)
        currentScore = countTriangles(currentState)
        bestState = currentState
        bestScore = currentScore
        temperature = startTemperature

        for j in range(iters):
            newState = nudge(currentState)
            newScore = countTriangles(newState)

            if(goalText == "MAXIMIZE"):
                if(newScore > currentScore):
                    currentState = newState
                    currentScore = newScore
                else:
                    prob = math.exp((newScore - currentScore) / temperature)
                    if(random.random() < prob):
                        currentState = newState
                        currentScore = newScore
            if(currentScore > bestScore):
                bestScore = currentScore
                bestState = currentState

            temperature *= coolingRate
    
        topResults = updateResults(topResults, bestState, bestScore)
    
    return topResults

def runAnnealingUntil(k, resetEvery, goalText, targetGap):
    ceiling = tamuraUpperBound(k)
    topResults = []

    currentState = createRandomState(k)
    currentScore = countTriangles(currentState)
    temperature = startTemperature

    iteration = 0

    while True:
        if((ceiling - currentScore) <= targetGap):
            print(f"Target gap of {targetGap} reached!!! Score: {currentScore} (Ceiling: {ceiling})")
            topResults = updateResults(topResults, currentState, currentScore)
            break

        if(iteration > 0 and iteration % resetEvery == 0):
            currentState = createRandomState(k)
            currentScore = countTriangles(currentState)
            temperature = startTemperature
        
        newState = nudge(currentState)
        newScore = countTriangles(newState)

        if(goalText == "MAXIMIZE"):
            if(newScore > currentScore):
                currentState = newState
                currentScore = newScore
            else:
                prob = math.exp((newScore - currentScore) / temperature)
                if(random.random() < prob):
                    currentState = newState
                    currentScore = newScore
        
        temperature *= coolingRate
        iteration += 1

    return topResults