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
class RoadPlanViewGeometryLine(object) :
    def __init__(self, xml_node):
        pass

class RoadPlanViewGeometrySpiral(object) :
    def __init__(self, xml_node):
        self.curvStart = xml_node.get("curvStart")
        self.curvEnd = xml_node.get("curvEnd")

class RoadPlanViewGeometryArc(object) :
    def __init__(self, xml_node):
        self.curvature = xml_node.get("curvature")

class RoadPlanViewGeometryPoly3(object):
    def __init__(self, xml_node):
        self.a = xml_node.get("a")
        self.b = xml_node.get("b")
        self.c = xml_node.get("c")
        self.d = xml_node.get("d")

class RoadPlanViewGeometryParamPoly3(object):
    def __init__(self, xml_node):
        self.aU = xml_node.get("aU")
        self.aV = xml_node.get("aV")
        self.bU = xml_node.get("bU")
        self.bV = xml_node.get("bV")
        self.cU = xml_node.get("cU")
        self.cV = xml_node.get("cV")
        self.dU = xml_node.get("dU")
        self.dV = xml_node.get("dV")
        self.pRange = xml_node.get("pRange")

class RoadPlanViewGeometryDescription(object) :
    def __init__(self, name, xml_node):
        if name == "line" :
            self.desc = None
            self.name = name
        elif name == "spiral" :
            self.desc = RoadPlanViewGeometrySpiral(xml_node)
            self.name = "spiral"
        elif name == "arc" :
            self.desc = RoadPlanViewGeometryArc(xml_node)
            self.name = "arc"
        elif name == "poly3" :
            self.desc = RoadPlanViewGeometryParamPoly3(xml_node)
            self.name = "poly3"
        elif name == "paramPoly3" :
            self.desc = RoadPlanViewGeometryParamPoly3(xml_node)
            self.name = "paramPoly3"
class RoadPlanViewGeometry(object):
    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.x = xml_node.get("x")
        self.y = xml_node.get("y")
        self.hdg = xml_node.get("hdg")
        self.length = xml_node.get("length")

        self.desc = RoadPlanViewGeometryDescription(xml_node.find("*").tag, xml_node.find("*"))




class RoadPlanView(object):
    def __init__(self, xml_node):
        self.geometry = [RoadPlanViewGeometry(i) for i in xml_node.findall("geometry")]
