import json
import os

node = hou.pwd()
geo = node.geometry()
fileName = node.evalParm("filePath")
baseFileName = os.path.basename(fileName)
geo.addAttrib(hou.attribType.Global, "mapName", "")
geo.setGlobalAttribValue("mapName", baseFileName.split(".")[0]);


def importJunctionConvex(junctions):
    geo.addAttrib(hou.attribType.Point, "boundJuctionId", 0)
    junctionBound_group = geo.createPointGroup("junctionBound")

    for junction in junctions:
        boundingPoly = junction["boundingPolygon"]
        junctionId = junction["junctionId"]

        for pt in boundingPoly:
            x = pt["x"]
            y = pt["z"]
            z = pt["y"]
            newPt = geo.createPoint()
            newPt.setPosition((x, y, z))
            newPt.setAttribValue("boundJuctionId", junctionId)
            junctionBound_group.add(newPt)


def addGeoAttrib():
    geo.addAttrib(hou.attribType.Point, "generatedFlag", False)
    # geo.addAttrib(hou.attribType.Point, "isInJunction", False)
    # geo.addAttrib(hou.attribType.Point, "junctionId", 0)

    geo.addAttrib(hou.attribType.Point, "assertPath", "")
    geo.addAttrib(hou.attribType.Point, "bpPath", "")
    geo.addAttrib(hou.attribType.Point, "laneName", "")
    geo.addAttrib(hou.attribType.Point, "laneType", 0)
    geo.addAttrib(hou.attribType.Point, "generatedFlagag", False)
    geo.addAttrib(hou.attribType.Point, "isInJunction", False)
    geo.addAttrib(hou.attribType.Point, "junctionId", 0)
    geo.addAttrib(hou.attribType.Point, "width", 0.0)

    geo.addAttrib(hou.attribType.Point, "roadId", 0)
    geo.addAttrib(hou.attribType.Point, "roadLength", 0.0)
    geo.addAttrib(hou.attribType.Point, "roadType", 0)
    geo.addAttrib(hou.attribType.Point, "sectionId", 0)

    geo.addAttrib(hou.attribType.Point, "partRowId", 0);
    geo.addAttrib(hou.attribType.Point, "partColId", 0);

    # 此字段用来记录道路连接关系
    # laneLink = lane["laneLink"]
    # left_laneName = laneLink["leftLaneName"]
    # right_laneName = laneLink["rightLaneName"]
    # predecessor = laneLink["preLanes"]
    # successor = laneLink["succLanes"]
    # geo.addAttrib(hou.attribType.Point, "laneLink", "")
    geo.addAttrib(hou.attribType.Point, "leftLaneName", "")
    geo.addAttrib(hou.attribType.Point, "rightLaneName", "")
    geo.addArrayAttrib(hou.attribType.Point, "predecessor", hou.attribData.String)
    geo.addArrayAttrib(hou.attribType.Point, "successor", hou.attribData.String)


def readOdSetting(file):
    # jsonObj = None
    # with open(file) as f :
    #     jsonObj = json.load(f)
    od_setting = jsonObj["odSetting"]
    gapToGeneratePillar = od_setting["gapToGeneratePillar"]
    gridSize = od_setting["gridSize"]
    leftUpBoundary = od_setting["leftUpBoundary"]
    lowestPoint = od_setting["lowestPoint"]
    odName = od_setting["odName"]
    rightDownBoundary = od_setting["rightDownBoundary"]
    geo.setGlobalAttribValue("leftUpBoundary", leftUpBoundary)


def readOD(file):
    jsonObj = None
    with open(file) as f:
        jsonObj = json.load(f)

    # handle od settings------------------------------------
    od_setting = jsonObj["odSetting"]
    gapToGeneratePillar = od_setting["gapToGeneratePillar"]
    gridSize = od_setting["gridSize"]
    leftUpBoundary = od_setting["leftUpBoundary"]
    leftUpBoundary = (leftUpBoundary["x"], leftUpBoundary["y"], leftUpBoundary["z"])
    lowestPoint = od_setting["lowestPoint"]
    lowestPoint = (lowestPoint["x"], lowestPoint["y"], lowestPoint["z"])
    odName = od_setting["odName"]
    rightDownBoundary = od_setting["rightDownBoundary"]
    rightDownBoundary = (rightDownBoundary["x"], rightDownBoundary["y"], rightDownBoundary["z"])

    catt = geo.addAttrib(hou.attribType.Global, "gapToGeneratePillar", 0.0)
    geo.setGlobalAttribValue(catt, gapToGeneratePillar)

    catt = geo.addAttrib(hou.attribType.Global, "leftUpBoundary", (0.0, 0, 0))
    geo.setGlobalAttribValue(catt, leftUpBoundary)

    catt = geo.addAttrib(hou.attribType.Global, "lowestPoint", (0.0, 0, 0))
    geo.setGlobalAttribValue(catt, lowestPoint)

    catt = geo.addAttrib(hou.attribType.Global, "odName", "")
    geo.setGlobalAttribValue(catt, odName)

    catt = geo.addAttrib(hou.attribType.Global, "rightDownBoundary", (0.0, 0, 0))
    geo.setGlobalAttribValue(catt, rightDownBoundary)

    catt = geo.addAttrib(hou.attribType.Global, "gridSize", 0.0);
    geo.setGlobalAttribValue(catt, gridSize)

    # handle roads data------------------------------------
    roads = jsonObj["roads"]
    if "junctions" in jsonObj:
        junctions = jsonObj["junctions"]
    else:
        junctions = []
    importJunctionConvex(junctions)
    right_group = geo.createPointGroup("right")
    left_group = geo.createPointGroup("left")
    middle_group = geo.createPointGroup("middle")

    road_right_group = geo.createPointGroup("roadright")
    road_left_group = geo.createPointGroup("roadleft")
    # refPoints_group = geo.createPointGroup("refPoints")

    for road in roads:
        primPts = []

        roadleft_pts = []
        roadright_pts = []
        # refPoints_pts = []
        # road data
        generatedFlag = road["generatedFlag"]
        isInJunction = road["isInJunction"]
        # junctionId = road["junctionId"]
        leftBoundaryPoints = road["leftBoundaryPoints"]
        rightBoundaryPoints = road["rightBoundaryPoints"]
        # refPoints = road["refPoints"]

        roadId = road["roadId"]
        col = road["partColId"]
        row = road["partRowId"]
        roadLength = road["roadLength"]
        roadType = road["roadType"]
        sectionId = road["sectionId"]
        rightBoundaryPoints.reverse()

        for rlbp in leftBoundaryPoints:
            x = rlbp["x"]
            y = rlbp["y"]
            z = rlbp["z"]

            pt = geo.createPoint()
            pt.setPosition((x, z, y))
            pt.setAttribValue("roadId", roadId)
            pt.setAttribValue("roadLength", roadLength)
            pt.setAttribValue("roadType", roadType)
            pt.setAttribValue("partColId", col)
            pt.setAttribValue("partRowId", row)
            pt.setAttribValue("junctionId", isInJunction)
            roadleft_pts.append(pt)
            road_left_group.add(roadleft_pts)

        for rrbp in rightBoundaryPoints:
            x = rrbp["x"]
            y = rrbp["y"]
            z = rrbp["z"]
            pt = geo.createPoint()
            pt.setPosition((x, z, y))
            pt.setAttribValue("roadId", roadId)
            pt.setAttribValue("roadLength", roadLength)
            pt.setAttribValue("roadType", roadType)
            pt.setAttribValue("partColId", col)
            pt.setAttribValue("partRowId", row)
            pt.setAttribValue("junctionId", isInJunction)
            roadright_pts.append(pt)
            road_right_group.add(roadright_pts)

        lanes = road["lanes"]


addGeoAttrib()
readOD(fileName)