import os
import sys
import numpy as np
from xml.etree.ElementTree import parse

import ODLane
import ODGeometry.RoadGeo as RoadGeo
import ODRoadLink.RoadLink as RoadLink


class RoadTypeSpeed(object):
    def __init__(self, xml_node):
        self.max = xml_node.get("max")
        self.unit = xml_node.get("unit")

class RoadType(object) :

    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.type = xml_node.get("type")
        self.country = xml_node.get("country")

        self.speed = RoadTypeSpeed(xml_node.find("speed"))

class Road(object) :
    def __init__(self, xml_node):
        self.id = xml_node.get("id")
        self.junction = xml_node.get("junction")
        self.length = xml_node.get("length")
        self.name = xml_node.get("name")

        self.road_type = [RoadType(i) for i in xml_node.findall("type")]
        # od package
        self.link = RoadLink.RoadLink(xml_node.find("link"))
        self.lanes = [ODLane.Lanes(i) for i in xml_node.findall("lanes")]

        # geo
        self.surface = RoadGeo.RoadSurface(xml_node.find("surface"))
        self.lateralProfile = RoadGeo.RoadLateralProfile(xml_node.find("lateralProfile"))
        self.elevationProfile = RoadGeo.RoadElevationProfile(xml_node.find("elevationProfile"))
        self.planView = RoadGeo.RoadPlanView(xml_node.find("planView"))






class testA(object) :

    def __init__(self):
        self.a = 5
        self.map = { "a" : self.a }

    def get_a(self):
        return self.a

if __name__ == "__main__" :
    file_name = "D:/Sim/from_shuyang/gicc/gicc.xodr"
    od = None
    with open(file_name, encoding="utf-8") as f:
        od = parse(f)

    road_array = od.findall("road")
    for road in road_array :
        current_road = Road(road)
        for road_type in current_road.road_type :
            print("current road : {} road type : {} {} {}".format(current_road.id, road_type.s, road_type.type, road_type.country));

