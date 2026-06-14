import dearpygui.dearpygui as dpg
import json
import math
import numpy as np
from pathlib import Path

ICON_PATH = Path(__file__).resolve().parents[1] / "Kobon.ico"

loadedData = []
currIdx = 0

blue = [(0, 125 + i * 10, 255, 100) for i in range(6)]

def nextIdx():
    global currIdx  # Fixed: matches currIdx
    if(currIdx + 1 < len(loadedData)):
        currIdx += 1
        updateView()

def prevIdx():
    global currIdx
    if(currIdx - 1 >= 0):
        currIdx -= 1
        updateView()

def loadJson(sender, appData):
    global loadedData, currIdx
    try:
        with open(appData['file_path_name'], 'r') as f:
            rawData = json.load(f)

        loadedData = rawData
        currIdx = 0
        updateView()
    except Exception as e:
        dpg.set_value("infoTxt", f"Error: {e}")

def getTriangles(lines):
    newAngle = []
    newOffset = []
    
    for i in lines:
        newAngle.append(i["angle"])
        newOffset.append(i["offset"])

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
    
    pointsOnLine = []

    for i in range(len(lines)):
        pointsOnLine.append([])
    
    for i in range(len(intersections)):
        currentIntersections = intersections[i]

        firstLine = currentIntersections[0]
        secondLine = currentIntersections[1]
        xCoord = currentIntersections[2]
        yCoord = currentIntersections[3]

        if(np.abs(a[firstLine]) < 0.5):
            pointsOnLine[firstLine].append((yCoord, i))
        else:
            pointsOnLine[firstLine].append((xCoord, i))
        
        if(np.abs(a[secondLine]) < 0.5):
            pointsOnLine[secondLine].append((yCoord, i))
        else:
            pointsOnLine[secondLine].append((xCoord, i))
        
    for i in range(len(pointsOnLine)):
        pointsOnLine[i].sort()
    
    sortedIndicesOnLine = []
    for i in range(len(pointsOnLine)):
        sortedIndicesOnLine.append([item[1] for item in pointsOnLine[i]])
    
    tris = []

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

                coord1 = (intersections[ijPoint][2], intersections[ijPoint][3])
                coord2 = (intersections[ikPoint][2], intersections[ikPoint][3])
                coord3 = (intersections[jkPoint][2], intersections[jkPoint][3])
                tris.append((coord1, coord2, coord3))

    return tris

def updateView():
    if not loadedData:
        return

    data = loadedData[currIdx]
    score = data.get('score', '?')

    txt = (
        f"Arrangement {currIdx + 1} / {len(loadedData)}\n"
        f"Triangles: {score}\n"
        f"Lines: {len(data['lines'])}"
    )

    dpg.set_value("infoTxt", txt)
    dpg.delete_item("canvas", children_only=True)

    triangles = getTriangles(data["lines"])

    center_x = 480 / 2
    center_y = 450 / 2
    
    for i, tri in enumerate(triangles):
        colorChoice = blue[i % len(blue)]

        pt1 = (center_x + tri[0][0] * 200, center_y + tri[0][1] * 200)
        pt2 = (center_x + tri[1][0] * 200, center_y + tri[1][1] * 200)
        pt3 = (center_x + tri[2][0] * 200, center_y + tri[2][1] * 200)

        dpg.draw_triangle(pt1,pt2,pt3,fill=colorChoice, color=(*colorChoice[:3], 255),thickness=1,parent="canvas")

    for i in data["lines"]:
        ang = math.radians(i["angle"])
        nx, ny = math.cos(ang), math.sin(ang)
        px, py = nx * i["offset"] * 200, ny * i["offset"] * 200

        x1 = center_x + px - ny * 1000
        y1 = center_y + py + nx * 1000
        x2 = center_x + px + ny * 1000
        y2 = center_y + py - nx * 1000

        dpg.draw_line((x1,y1),(x2,y2),color=(255,255,255,255),thickness=2,parent="canvas")

        json_str = json.dumps(data, indent=2)
        dpg.set_value("jsonTxt", json_str)

dpg.create_context()

with dpg.window(label="Instructions (usage guide)", modal=True, show=True, tag="popup", width=600, height=400, pos=[100, 100], no_resize=True, no_move=True):
    

    with dpg.child_window(height=-40, border=False):
        dpg.add_text(
            "Welcome to Project Kobon's output viewer! \n \n"
            
            "Import the file your Discord Webhook outputed into the imports field (right side)\n"
            "to view it."
        )

    dpg.add_separator()
    dpg.add_button(label="Close", width=-1, callback=lambda: dpg.configure_item("popup", show=False))

with dpg.window(tag="main", label="Project Kobon Viewer"):
    with dpg.group(horizontal=True):
        with dpg.child_window(width=500, height=500):
            dpg.add_text("Visualizer Canvas")
            dpg.add_separator()
            
            with dpg.drawlist(width=480, height=450, tag="canvas"):
                pass
            
        with dpg.child_window(width=260, height=500):
            dpg.add_button(label="Import JSON File", callback=lambda: dpg.show_item("fileDialog"), width=-1)
            dpg.add_text("JSON Data:", color=(200, 200, 200))
            with dpg.child_window(height=250):
                dpg.add_text("", tag="jsonTxt", wrap=230)
            dpg.add_spacer(height=5)
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="<- Prev", callback=prevIdx, width=110)
                dpg.add_button(label="Next ->", callback=nextIdx, width=110)
            
            dpg.add_spacer(height=5)
            dpg.add_text("No data loaded...", tag="infoTxt", wrap=240)

with dpg.file_dialog(show=False, callback=loadJson, tag="fileDialog", width=400, height=300):
    dpg.add_file_extension(".json", color=(0, 255, 0, 255))

dpg.create_viewport(title="Project Kobon", width=800, height=555, small_icon=str(ICON_PATH), large_icon=str(ICON_PATH))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()