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