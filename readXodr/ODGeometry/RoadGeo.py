#surface
class RoadSurfaceCRG(object):
    def __init__(self, xml_node):
        self.file = xml_node.get("file")
        self.sStart = xml_node.get("sStart")
        self.sEnd = xml_node.get("sEnd")
        self.orientation = xml_node.get("orientation")
        self.mode = xml_node.get("mode")
        self.purpose = xml_node.get("purpose")
        self.sOffset = xml_node.get("sOffset")
        self.tOffset = xml_node.get("tOffset")
        self.zOffset = xml_node.get("zOffset")
        self.zScale = xml_node.get("zScale")

class RoadSurface(object) :
    def __init__(self, xml_node):
        if xml_node :
            self.CRG = [RoadSurfaceCRG(i) for i in xml_node.findall("CRG")]



#elecationProfile
class RoadElevationProfileElevation(object) :
    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.a = xml_node.get("a")
        self.b = xml_node.get("b")
        self.c = xml_node.get("c")
        self.d = xml_node.get("d")


class RoadElevationProfile(object):
    def __init__(self, xml_node):
        self.elevation = [RoadElevationProfileElevation(i) for i in xml_node.findall("elevation")]

#superelevation

class RoadLateralProfileSuperelevation(object):
    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.a = xml_node.get("a")
        self.b = xml_node.get("b")
        self.c = xml_node.get("c")
        self.d = xml_node.get("d")

class RoadLateralProfileShape(object):
    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.t = xml_node.get("t")
        self.a = xml_node.get("a")
        self.b = xml_node.get("b")
        self.c = xml_node.get("c")
        self.d = xml_node.get("d")

class RoadLateralProfile(object) :
    def __init__(self, xml_node):
        self.superelevation = [RoadLateralProfileSuperelevation(i) for i in xml_node.findall("superelevation")]
        self.shape = [RoadLateralProfileShape(i) for i in xml_node.findall("shape")]


#geometry
class RoadPlanViewGeometry(object):
    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.x = xml_node.get("x")
        self.y = xml_node.get("y")
        self.hdg = xml_node.get("hdg")
        self.length = xml_node.get("length")

class RoadPlanView(object):
    def __init__(self, xml_node):
        self.geometry = [RoadPlanViewGeometry(i) for i in xml_node.findall("geometry")]
