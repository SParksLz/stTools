
import os
import sys
import numpy as np
from xml.etree.ElementTree import parse


link_template = {
    "contactPoint": None,
    "elementId": None,
    "elementType": None
}

class LaneOffset(object):
    def __init__(self, lane_offset_xml):
        self.offset_a = lane_offset_xml.get("a")
        self.offset_b = lane_offset_xml.get("b")
        self.offset_c = lane_offset_xml.get("c")
        self.offset_d = lane_offset_xml.get("d")
        self.offset_s = lane_offset_xml.get("s")


class LaneSection(object):
    def __init__(self, section_xml, laneOffset):
        self.__section_xml = section_xml
        self.__s = section_xml.get("s")
        self.__single_side = section_xml.get("singleSide")
        self.__center = section_xml.find("center")
        self.__right = section_xml.find("right")
        self.__left = section_xml.find("left")
        self.__laneOffset = laneOffset

    def compute_geometry(self):






class Lane(object):
    def __init__(self, lane_xml):
        self.__lane = lane_xml
        self.__lane_offset = LaneOffset(lane_xml.find("laneOffset"))

    def __get_sections(self):
        return self.__lane.findall("laneSection")

    def __get_offset(self):
        return self.__lane_offset

    def __parse_section(self, section):
        s = section.get("s")
        single_side = section.get("singleSide")
        return section.findall("*")

    def section_log(self):
        pass

    def compute_position(self):
        for section in self.__get_sections():
            current_section = LaneSection(section, self.__lane_offset)
            print(current_section.compute_geometry())









def od_reader(file):
    with open(file, encoding="utf-8") as f:
        # print(f)
        od = parse(f)
        root = od.getroot()
        roads = root.findall("road")
        for road in roads:
            road_id = int(road.get("id"))
            road_length = road.get("length")
            road_junction = int(road.get("junction"))

            road_name = road.get("name")
            road_type = road.find("type")
            road_type_s = road_type.get("s")
            road_type_type = road_type.get("type")

            road_type_speed = road_type.find("speed")
            road_type_speed_max = road_type_speed.get("max")
            road_type_speed_unit = road_type_speed.get("unit")

            road_plan_view = road.find("planView")
            road_pv_geometry = road_plan_view.findall("geometry")

            road_lanes = road.find("lanes")

            lane = Lane(road_lanes)
            lane.compute_position()
            # lane.section_log()




            # print(road_lanes)

            # lane_sections = road_lanes.findall("laneSection")

            road_predecessor = []
            road_successor = []

            temp = link_template

            link = road.find("link")
            try:
                link_predecessors = link.findall("predecessor")
            except:
                # print("{} has not predecessor".format(road_id))
                link_predecessors = []
            try:
                link_successors = link.findall("successor")
            except:
                # print("{} has not successor".format(road_id))
                link_successors = []
            if len(link_predecessors) > 0:
                for pre in link_predecessors:
                    for k in link_template:
                        temp[k] = pre.get(k)
                    road_predecessor.append(temp)
                    temp = link_template
            if len(link_successors) > 0:
                for suc in link_successors:
                    for k in link_template:
                        temp[k] = pre.get(k)
                    temp = link_template
                    road_successor.append(temp)

            # print(road_successor)
            # print(road_predecessor)

            for geo in road_pv_geometry:
                delta_s = 1

                geo_length = float(geo.get("length"))
                geo_s = float(geo.get("s"))
                geo_x = float(geo.get("x"))
                geo_y = float(geo.get("y"))
                hdg = float(geo.get("hdg"))

                count = max(int(geo_length / delta_s), 5)
                # count = int(geo_length / delta_s)
                delta_normalize = 1.0 / count

                geo_start_p = np.array([geo_x, hdg, geo_y])

                sub_geo = geo.findall("*")
                # road modeling
                for poly3 in sub_geo:
                    if poly3.tag == "paramPoly3":
                        a_u = float(poly3.get("aU"))
                        a_v = float(poly3.get("aV"))
                        b_u = float(poly3.get("bU"))
                        b_v = float(poly3.get("bV"))
                        c_u = float(poly3.get("cU"))
                        c_v = float(poly3.get("cV"))
                        d_u = float(poly3.get("dU"))
                        d_v = float(poly3.get("dV"))
                        p_range = poly3.get("pRange")
                        for i in range(0, count):
                            t = delta_normalize * i
                            u = a_u + b_u * t + c_u * t * t + d_u * t * t * t
                            v = a_v + b_v * t + c_v * t * t + d_v * t * t * t

                            du_dt = b_u + 2 * c_u * t + 3 * d_u * t * t
                            dv_dt = b_v + 2 * c_v * t + 3 * d_v * t * t

                            new_hdg = np.arctan2(dv_dt, du_dt)

                            new_pos = np.array([u, 0, v])

                # lanes modeling



class Road(object):
    def __init__(self):
        # base attr
        self.roadId = None
        self.junction = None
        self.length = None
        self.name = None
        # link
        self.predecessor = link_template
        self.successor = link_template

    def set_link_info(self, link_info):
        pass


od_file = "G:\\gitpool\\sparksTools\\stForHoudini\\ODReader\\sampler\\CityScape6.xodr"
od_reader(od_file)
