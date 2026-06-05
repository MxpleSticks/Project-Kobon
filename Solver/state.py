import random
from dataclasses import dataclass

@dataclass
class LineState:
    angle: float
    offset: float

def create_random_state(k):
    lines = []

    for i in range(k):
        angle = random.uniform(0,180)
        offset = random.uniform(-1,1)
        lines.append(LineState(angle, offset))
    
    return lines

def nudge(lines):
    nudgedLines = []

    for i in lines:
        nudgedLines.append(LineState(i.angle, i.offset))

    change = random.randrange(0,len(nudgedLines))
    chosenLine = nudgedLines[change]
    
    angleOrOffset = random.randrange(0,2)

    if(angleOrOffset == 1):
        chosenLine.angle += random.uniform(-0.5,0.5)
        chosenLine.angle = chosenLine.angle % 180
    else:
        chosenLine.offset += random.uniform(-0.05,0.05)
        chosenLine.offset = max(-1, min(1, chosenLine.offset))

    return nudgedLines