import numpy as np

def count_triangles(lines):
    newAngle = []
    newOffset = []
    
    for i in lines:
        newAngle.append(i.angle)
        newOffset.append(i.offset)

    AngleDegrees = np.array(newAngle)
    Offset = np.array(newOffset)

    AngleRadians = AngleDegrees * (np.pi / 180)

    a = np.cos(AngleRadians)
    b = np.sin(AngleRadians)
    c = Offset

    intersections = []

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            firstEq = a[i], b[i], c[i]
            secondEq = a[j], b[j], c[j]
            determinant = firstEq[0]*secondEq[1] - firstEq[1]*secondEq[0]

            if(np.abs(determinant) < 0.0001):
                continue

            x = (firstEq[2]*secondEq[1] - firstEq[1]*secondEq[2]) / determinant
            y = (firstEq[0]*secondEq[2] - firstEq[2]*secondEq[0]) / determinant

            intersections.append((i, j, x, y))
    
    points = []

    for i, j, x, y in intersections:
        points.append((x, y))
    
    pointsOnLine = []

    for i in range(len(lines)):
        pointsOnLine.append([])

    for i in range(len(intersections)):
        currentIntersection = intersections[i]

        firstLine = currentIntersection[0]
        secondLine = currentIntersection[1]

        pointsOnLine[firstLine].append(i)
        pointsOnLine[secondLine].append(i)
    
    for i in range(len(pointsOnLine)):
        pointsOnLine[i]