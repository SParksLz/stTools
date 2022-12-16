import json

node = hou.pwd()
import json

node = hou.pwd()
geo = node.geometry()
fileName = node.evalParm("filePath")


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

    geo.addAttrib(hou.attribType.Point, "roadId", 0)
    geo.addAttrib(hou.attribType.Point, "roadLength", 0.0)
    geo.addAttrib(hou.attribType.Point, "roadType", 0)
    geo.addAttrib(hou.attribType.Point, "sectionId", 0)

def createBound(jsonObj) :
    od_setting = jsonObj["odSetting"]
    left_bound_point = od_setting["leftUpBoundary"]
    right_bound_point = od_setting["rightDownBoundary"]

    lbx = left_bound_point["x"]
    lby = left_bound_point["y"]
    lbz = left_bound_point["z"]

    rbx = right_bound_point["x"]
    rby = right_bound_point["y"]
    rbz = right_bound_point["z"]

    lb_pt = geo.createPoint()
    lb_pt.setPosition((lbx, lbz,lby))

    rb_pt = geo.createPoint()
    rb_pt.setPosition((rbx, rbz,rby))






def readOD(file):
    jsonObj = None
    with open(file) as f:
        jsonObj = json.load(f)

    createBound(jsonObj)
    roads = jsonObj["roads"]
    right_group = geo.createPointGroup("right")
    left_group = geo.createPointGroup("left")
    middle_group = geo.createPointGroup("middle")

    road_right_group = geo.createPointGroup("roadright")
    road_left_group = geo.createPointGroup("roadleft")




    for road in roads:
        primPts = []

        roadleft_pts = []
        roadright_pts = []
        # road data
        generatedFlag = road["generatedFlag"]
        # isInJunction = road["isInJunction"]
        # junctionId = road["junctionId"]
        leftBoundaryPoints = road["leftBoundaryPoints"]
        rightBoundaryPoints = road["rightBoundaryPoints"]
        roadId = road["roadId"]
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
            roadleft_pts.append(pt)
            road_left_group.add(roadleft_pts)

        for rrbp in rightBoundaryPoints:
            x = rrbp["x"]
            y = rrbp["y"]
            z = rrbp["z"]
            pt = geo.createPoint()
            pt.setPosition((x, z, y))
            pt.setAttribValue("roadId", roadId)
            roadright_pts.append(pt)
            road_right_group.add(roadright_pts)

        lanes = road["lanes"]

        left_pts = []
        right_pts = []
        middle_pts = []

        for lane in lanes:
            # lane data
            leftBoundaryPoints = lane["leftBoundaryPoints"]
            rightBoundaryPoints = lane["rightBoundaryPoints"]
            isInJunction = lane["isInJunction"]
            junctionId = lane["junctionId"]
            middlePoints = lane["middlePoints"]
            assetPath = lane["assertPath"]
            bpPath = lane["bpPath"]
            laneName = lane["laneName"]
            laneType = lane["laneType"]
            rightBoundaryPoints.reverse()

            for lbp in leftBoundaryPoints:
                x = lbp["x"]
                y = lbp["y"]
                z = lbp["z"]

                pt = geo.createPoint()
                pt.setPosition((x, z, y))
                pt.setAttribValue("assertPath", assetPath)
                pt.setAttribValue("bpPath", bpPath)
                pt.setAttribValue("laneName", laneName)
                pt.setAttribValue("laneType", laneType)
                pt.setAttribValue("generatedFlag", generatedFlag)
                pt.setAttribValue("isInJunction", isInJunction)
                pt.setAttribValue("junctionId", junctionId)

                pt.setAttribValue("roadId", roadId)
                pt.setAttribValue("roadLength", roadLength)
                pt.setAttribValue("roadType", roadType)
                pt.setAttribValue("sectionId", sectionId)
                left_pts.append(pt)
                left_group.add(left_pts)

            for rbp in rightBoundaryPoints:
                x = rbp["x"]
                y = rbp["y"]
                z = rbp["z"]

                pt = geo.createPoint()
                pt.setPosition((x, z, y))
                pt.setAttribValue("assertPath", assetPath)
                pt.setAttribValue("bpPath", bpPath)
                pt.setAttribValue("laneName", laneName)
                pt.setAttribValue("laneType", laneType)
                pt.setAttribValue("generatedFlag", generatedFlag)
                pt.setAttribValue("isInJunction", isInJunction)
                pt.setAttribValue("junctionId", junctionId)

                pt.setAttribValue("roadId", roadId)
                pt.setAttribValue("roadLength", roadLength)
                pt.setAttribValue("roadType", roadType)
                pt.setAttribValue("sectionId", sectionId)

                right_pts.append(pt)
                right_group.add(right_pts)

            for mp in middlePoints:
                x = mp["x"]
                y = mp["y"]
                z = mp["z"]

                pt = geo.createPoint()
                pt.setPosition((x, z, y))
                pt.setAttribValue("assertPath", assetPath)
                pt.setAttribValue("bpPath", bpPath)
                pt.setAttribValue("laneName", laneName)
                pt.setAttribValue("laneType", laneType)
                pt.setAttribValue("generatedFlag", generatedFlag)
                pt.setAttribValue("isInJunction", isInJunction)
                pt.setAttribValue("junctionId", junctionId)

                pt.setAttribValue("roadId", roadId)
                pt.setAttribValue("roadLength", roadLength)
                pt.setAttribValue("roadType", roadType)
                pt.setAttribValue("sectionId", sectionId)
                middle_pts.append(pt)
                middle_group.add(middle_pts)

        primPts.append(left_pts)
        primPts.append(right_pts[-1:0])

        primPts.append(roadleft_pts)
        primPts.append(roadright_pts[-1:0])

        # right_pts_re = right_pts.reverse()

        poly = geo.createPolygon(primPts)


addGeoAttrib()
readOD(fileName)