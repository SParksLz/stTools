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

        speed_node = xml_node.find("speed")
        if speed_node :
            self.speed = RoadTypeSpeed(speed_node)
        else :
            self.speed = None

class Road(object) :
    def __init__(self, xml_node):
        self.id = xml_node.get("id")
        self.junction = xml_node.get("junction")
        self.length = xml_node.get("length")
        self.name = xml_node.get("name")

        self.road_type = [RoadType(i) for i in xml_node.findall("type")]
        # od package
        link_node = xml_node.find("link")
        if link_node :
            self.link = RoadLink.RoadLink(link_node)
        else :
            self.link = None
        # self.lanes = [ODLane.Lanes(i) for i in xml_node.findall("lanes")]
        self.lanes = ODLane.Lanes(xml_node.find("lanes"))

        # geo
        surface_node = xml_node.find("surface")
        lateralProfile_node = xml_node.find("lateralProfile")
        elevationProfile_node = xml_node.find("elevationProfile")

        if surface_node :
            self.surface = RoadGeo.RoadSurface(surface_node)
        else :
            self.surface = None
        if lateralProfile_node :
            self.lateralProfile = RoadGeo.RoadLateralProfile(lateralProfile_node)
        else :
            self.lateralProfile = None

        if elevationProfile_node :
            self.elevationProfile = RoadGeo.RoadElevationProfile(elevationProfile_node)
        else :
            self.elevationProfile = None

        self.planView = RoadGeo.RoadPlanView(xml_node.find("planView"))






class testA(object) :

    def __init__(self):
        self.a = 5
        self.map = { "a" : self.a }

    def get_a(self):
        return self.a

if __name__ == "__main__" :
    file_name = "../gicc.xodr"
    od = None
    with open(file_name, encoding="utf-8") as f:
        od = parse(f)


    road_array = od.findall("road")
    for road in road_array :
        current_road = Road(road)
        print("----------------------{}-------------------".format(current_road.id))
        current_lanes = current_road.lanes
        for s in current_lanes.laneSection :
            print("    ---left---")
            if s.left :
                for lane in s.left.lane :
                    print(lane)
            print("    ---right---")
            if s.right :
                for lane in s.right.lane :
                    print(lane)

            print("    ---center---")
            print(s.center.lane)




        # for road_type in current_road.road_type :
        #     print("current road : {} road type : {} {} {}".format(current_road.id, road_type.s, road_type.type, road_type.country));


