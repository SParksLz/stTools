import os
import sys
from xml.etree.ElementTree import parse

link_template = {
    "contactPoint": None,
    "elementId": None,
    "elementType": None
}


def od_reader(file):
    with open(file, encoding="utf-8") as f:
        od = parse(f)
        root = od.getroot()
        roads = root.findall("road")
        for road in roads:
            road_id = road.get("id")
            road_length = road.get("length")
            road_junction = road.get("junction")
            road_name = road.get("name")

            road_predecessor = []
            road_successor = []

            temp = link_template

            link = road.find("link")
            try :
                link_predecessors = link.findall("predecessor")
                link_successors = link.findall("successor")
            except :
                print(road_id)
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
            # print(link_predecessors)
            # print(link_successors)



class Lane(object):
    def __init__(self):
        pass


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






if __name__ == "__main__":
    current_path = os.path.abspath(".")
    od_file = os.path.join(current_path, "sampler\\CityScape6.xodr")
    od_reader(od_file)
