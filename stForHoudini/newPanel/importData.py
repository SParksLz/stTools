from xml.etree import ElementTree
import math


def transformlat(lng, lat):
    PI = 3.1415926535897932384626
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * \
          lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 *
            math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * PI) + 40.0 *
            math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * PI) + 320 *
            math.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    PI = 3.1415926535897932384626
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 *
            math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * PI) + 40.0 *
            math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 *
            math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret


class nodeBase(object):

    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def gcj02towgs84(self):
        lng = self.lon
        lat = self.lat
        PI = 3.1415926535897932384626
        ee = 0.00669342162296594323
        a = 6378245.0
        dlat = transformlat(lng - 105.0, lat - 35.0)
        dlng = transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * PI
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * PI)
        mglat = lat + dlat
        mglng = lng + dlng
        return str(lng * 2 - mglng) + ',' + str(lat * 2 - mglat)


class wayBase(object):
    def __init__(self, nodeList, relationDir):
        self.nodeList = nodeList
        self.relationDir = relationDir


xmlFileName = r"G:\51liuzhen\AES_V1_PaaS\Plugins\AesTiles\Content\Maps\shanghai_L3_modular\AES_DATA\Vector\10\Tile_35B2690000000000_Buildings.xml"
tree = ElementTree.parse(xmlFileName)

root = tree.getroot()
children = root.getchildren()
nodeList = root.findall("node")

way = root.findall("way")
way = way[0:8000]
wayList = []
# print "start build way...."
for i in way:
    id = i.get("id")
    # print id
    relation_dir = {}
    relation_tree = root.find("./relation/member[@ref='{0}']".format(id))
    relation_tag = relation_tree.findall("tag")
    for rt in relation_tag:
        relation_dir[rt.get("k")] = rt.get("v")
    tag_dir = {}
    node_dir = {}
    nodeList = []
    tagList = i.findall("tag")
    ndList = i.findall("nd")
    for tag in tagList:
        tag_dir[tag.get("k")] = tag.get("v")
        # print tag_dir
    for nd in ndList:
        current_id = nd.get("ref")
        spe_node = root.find("./node[@id='{0}']".format(current_id))
        node = nodeBase(float(spe_node.get("lat")), \
                        float(spe_node.get("lon")), \
                        float(spe_node.get("alt")))
        nodeList.append(node)
    currentWay = wayBase(nodeList, relation_dir)
    currentWay.color = tag_dir["RoofColor"]
    currentWay.height = tag_dir["height"]
    currentWay.id = id
    wayList.append(currentWay)

# print "build complete"
node = hou.pwd()
geo = node.geometry()

geo.addAttrib(hou.attribType.Point, "color_string", "")
geo.addAttrib(hou.attribType.Point, "height_string", "")
geo.addAttrib(hou.attribType.Point, "wayId", "")

for w in wayList:
    pt_list = []
    nodeList = w.nodeList
    nodeList.reverse()
    relation = w.relationDir

    for n in nodeList:
        pos = n.gcj02towgs84()
        print pos
        x = float(pos.split(",")[0])
        z = float(pos.split(",")[1])
        pt = geo.createPoint()
        pt.setPosition((x, 0, z))
        pt_list.append(pt)
        # geo.addAttrib(hou.attribType.Point, "color_string", "")
        # geo.addAttrib(hou.attribType.Point, "height_string", "")
        pt.setAttribValue("color_string", w.color)
        pt.setAttribValue("height_string", w.height)
        pt.setAttribValue("wayId", w.id)

# Add code to modify contents of geo.
# Use drop down menu to select examples.
