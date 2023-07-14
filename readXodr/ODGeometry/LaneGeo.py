class LaneOffset(object) :
    def __init__(self, xml_node):
        self.s = xml_node.get("s")
        self.a = xml_node.get("a")
        self.b = xml_node.get("b")
        self.c = xml_node.get("c")
        self.d = xml_node.get("d")


class LaneSectionLRLaneHeight(object):
    def __init__(self, xml_node):
        self.sOffset = xml_node.get("sOffset")
        self.inner = xml_node.get("inner")
        self.outer = xml_node.get("outer")

class LaneSectionLRLaneWidth(object):
    def __init__(self, xml_node):
        self.sOffset = xml_node.get("sOffset")
        self.a = xml_node.get("a")
        self.b = xml_node.get("b")
        self.c = xml_node.get("c")
        self.d = xml_node.get("d")

class LaneSectionLRLaneBorder(object):
    def __init__(self, xml_node):
        self.sOffset = xml_node.get("sOffset")
        self.a = xml_node.get("a")
        self.b = xml_node.get("b")
        self.c = xml_node.get("c")
        self.d = xml_node.get("d")


