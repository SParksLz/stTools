import os
import hou
import json

node = hou.pwd()
geo = node.geometry()

output_name = node.evalParm("output")
dir_name = os.path.dirname(output_name)
file_name = os.path.basename(output_name)

# Add code to modify contents of geo.
# Use drop down menu to select examples.

elementsDir = {}

allpts = geo.points()
for pt in allpts :
    currentElement = {}
    p = pt.attribValue("P")
    unreal_instance = pt.attribValue("unreal_instance")
    instance_name = pt.attribValue("unreal_instancename")
    scale = pt.attribValue("scale")
    rotate = pt.attribValue("rotation")
    currentElement["path"] = unreal_instance
    currentElement["pos"]["x"] = p[0]
    currentElement["pos"]["y"] = p[1]
    currentElement["pos"]["z"] = p[2]

    currentElement["rotation"]["x"] = rotate[0]
    currentElement["rotation"]["y"] = rotate[1]
    currentElement["rotation"]["z"] = rotate[2]

    currentElement["scale"]["x"] = scale[0]
    currentElement["scale"]["y"] = scale[1]
    currentElement["scale"]["z"] = scale[2]

with open(output_name, "w", encoding='utf-8') as f:
    json.dump(output_name, f, indent=2, sort_keys=True, ensure_ascii=False)





