


class RoadLinkPS(object):
    def __init__(self, xml_node):
        self.elementId = xml_node.get("elementId")
        self.elementType = xml_node.get("elementType")
        self.contactPoint = xml_node.get("contactPoint")
        self.elementS = xml_node.get("elementS")
        self.elementDir = xml_node.get("elementDir")

class RoadLinkPredecessor(RoadLinkPS) :
    def __init__(self, xml_node):
        super().__init__(xml_node)

class RoadLinkPredecessor(RoadLinkPS) :
    def __init__(self, xml_node):
        super().__init__(xml_node)

class RoadLink(object):
    def __init__(self, xml_node):
        self.predecessor = RoadLinkPredecessor(xml_node.find("predecessor"))
        self.successor = RoadLinkPredecessor(xml_node.find("successor"))