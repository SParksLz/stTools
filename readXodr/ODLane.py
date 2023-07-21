from readXodr.ODGeometry import LaneGeo

#----
class LaneSectionLrLane_Material(object) :
    def __init__(self, xml_node):
        self.sOffset = xml_node.get("sOffset")
        self.surface = xml_node.get("surface")
        self.friction = xml_node.get("friction")
        self.roughness = xml_node.get("roughness")

class LaneSectionLrLane_Speed(object) :
    def __init__(self, xml_node):
        self.sOffset = xml_node.get("sOffset")
        self.max = xml_node.get("max")
        self.unit = xml_node.get("unit")

class LaneSectionLrLane_Access(object) :
    def __init__(self, xml_node):
        self.sOffset = xml_node.get("sOffset")
        self.rule = xml_node.get("rule")
        self.restriction = xml_node.get("restriction")


class LaneSectionLcrLane_RoadMark(object) :
    def __init__(self, xml_node):
        pass

class LaneSectionLrLane_Rule(object) :
    def __init__(self, xml_node):
        self.sOffset = xml_node.get("sOffset")
        self.value = xml_node.get("value")

#----link
class LaneSectionLcrLaneLink(object) :
    def __init__(self, xml_node):
        self.predecessor = [LaneSectionLcrLaneLink_Predecessor(i) for i in xml_node.findall("predecessor")]
        self.successor = [LaneSectionLcrLaneLink_Successor(i) for i in xml_node.findall("successor")]

class LaneSectionLcrLaneLink_ps(object) :
    def __init__(self, xml_node):
        self.id = xml_node

class LaneSectionLcrLaneLink_Predecessor(LaneSectionLcrLaneLink_ps) :
    def __init__(self, xml_node):
        super(LaneSectionLcrLaneLink_Predecessor, self).__init__(xml_node)

class LaneSectionLcrLaneLink_Successor(LaneSectionLcrLaneLink_ps) :
    def __init__(self, xml_node):
        super(LaneSectionLcrLaneLink_Successor, self).__init__(xml_node)

class LaneSectionCenterLane(object):
    def __init__(self, xml_node):
        self.id = 0;
        self.type = None
        self.level = False

        # lane info
        self.roadMark = [LaneSectionLcrLane_RoadMark(i) for i in xml_node.findall("roadMark") ]  # lrc
        #link
        link_node = xml_node.find("link")
        if link_node :
            self.link = LaneSectionLcrLaneLink(link_node)
        else :
            self.link = None

class LaneSectionLRLane(object):
    def __init__(self, xml_node):
        self.id = xml_node.get("id")
        self.level = xml_node.get("level")
        self.type = xml_node.get("type")

        #geometry info
        self.height = [LaneGeo.LaneSectionLRLaneHeight(i) for i in xml_node.findall("height")]
        self.width = [LaneGeo.LaneSectionLRLaneWidth(i) for i in xml_node.findall("width")]
        self.border = [LaneGeo.LaneSectionLRLaneBorder(i) for i in xml_node.findall("border")]

        #lane info
        self.access = [LaneSectionLrLane_Access(i) for i in xml_node.findall("access")]
        self.rule = [LaneSectionLrLane_Rule(i) for i in xml_node.findall("rule")]
        self.material = [LaneSectionLrLane_Material(i) for i in xml_node.findall("material")]
        self.speed = [LaneSectionLrLane_Speed(i) for i in xml_node.findall("speed")]
        self.roadMark = [LaneSectionLcrLane_RoadMark(i) for i in xml_node.findall("roadMark")] #lrc

        #link info
        link_node = xml_node.find("link")
        if link_node :
            self.link = LaneSectionLcrLaneLink(link_node)
        else:
            self.link = None


class LaneSectionCenter(object):
    def __init__(self, xml_node):
        self.lane = LaneSectionCenterLane(xml_node.find("lane"))

class LaneSectionLR(object) :
    def __init__(self, xml_node):
        self.lane = [LaneSectionLRLane(i) for i in xml_node.findall("lane")]

class LaneSectionLeft(LaneSectionLR):
    def __init__(self, xml_node):
        super(LaneSectionLeft, self).__init__(xml_node)

class LaneSectionRight(LaneSectionLR):
    def __init__(self, xml_node):
        super(LaneSectionRight, self).__init__(xml_node)

class LaneSection(object) :
    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.singleSide = xml_node.get("singleSide")

        self.center = LaneSectionCenter(xml_node.find("center"))

        left_node = xml_node.find("left")
        right_node = xml_node.find("right")
        if left_node:
            self.left = LaneSectionLeft(left_node)
        else :
            self.left = None

        if right_node:
            self.right = LaneSectionRight(right_node)
        else :
            self.right = None

class Lanes(object):
    def __init__(self, xml_node):
        self.laneOffset = [LaneGeo.LaneOffset(i) for i in xml_node.findall("laneOffset")]
        self.laneSection = [LaneSection(i) for i in xml_node.findall("laneSection")]



