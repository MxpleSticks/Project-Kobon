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
        xCoord = currentIntersection[2]
        yCoord = currentIntersection[3]

        if np.abs(a[firstLine]) < 0.5:
            pointsOnLine[firstLine].append((yCoord, i))
        else:
            pointsOnLine[firstLine].append((xCoord, i))

        if np.abs(a[secondLine]) < 0.5:
            pointsOnLine[secondLine].append((yCoord, i))
        else:
            pointsOnLine[secondLine].append((xCoord, i))
    
    for i in range(len(pointsOnLine)):
        pointsOnLine[i].sort()

    sortedIndicesOnLine = []
    for i in range(len(pointsOnLine)):
        sortedIndicesOnLine.append([item[1] for item in pointsOnLine[i]])
    
    triangleCount = 0

    for i in range(len(sortedIndicesOnLine)):
        for j in range(i + 1, len(sortedIndicesOnLine)):
            for k in range(j + 1, len(sortedIndicesOnLine)):
                ijPoint = None
                ikPoint = None
                jkPoint = None

                for h in range(len(intersections)):
                    currentIntersection = intersections[h]

                    firstLine = currentIntersection[0]
                    secondLine = currentIntersection[1]

                    if(firstLine == i and secondLine == j):
                        ijPoint = h
                    elif(firstLine == i and secondLine == k):
                        ikPoint = h
                    elif(firstLine == j and secondLine == k):
                        jkPoint = h
                
                if(ijPoint == None or ikPoint == None or jkPoint == None):
                    continue

                ijPosition = sortedIndicesOnLine[i].index(ijPoint)
                ikPosition = sortedIndicesOnLine[i].index(ikPoint)

                if(np.abs(ijPosition - ikPosition) != 1):
                    continue

                ijPosition = sortedIndicesOnLine[j].index(ijPoint)
                jkPosition = sortedIndicesOnLine[j].index(jkPoint)

                if(np.abs(ijPosition - jkPosition) != 1):
                    continue

                ikPosition = sortedIndicesOnLine[k].index(ikPoint)
                jkPosition = sortedIndicesOnLine[k].index(jkPoint)

                if(np.abs(ikPosition - jkPosition) != 1):
                    continue

                triangleCount += 1
    
    return triangleCount