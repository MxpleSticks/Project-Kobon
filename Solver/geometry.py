import cupy as cp

def count_triangles(lines):
    newAngle = []
    newOffset = []
    
    for i in lines:
        newAngle.append(i.angle)
        newOffset.append(i.offset)

    cpAngleDegrees = cp.array(newAngle)
    cpOffset = cp.array(newOffset)

    cpAngleRadians = cpAngleDegrees * (cp.pi / 180)

    a = cp.cos(cpAngleRadians)
    b = cp.sin(cpAngleRadians)
    c = cpOffset

    intersections = []

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            firstEq = a[i], b[i], c[i]
            secondEq = a[j], b[j], c[j]
            determinant = firstEq[0]*secondEq[1] - firstEq[1]*secondEq[0]

            if(cp.abs(determinant) < 0.0001):
                continue

            x = (firstEq[2]*secondEq[1] - firstEq[1]*secondEq[2]) / determinant
            y = (firstEq[0]*secondEq[2] - firstEq[2]*secondEq[0]) / determinant

            intersections.append((i, j, x, y))

