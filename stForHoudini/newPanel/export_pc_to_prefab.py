import os
import sys
import hou
import json


# nodePath = "/obj/UHA_Building_Body_Generator/UHA_Building_Body_Generator1/Roof/RoofTop_PC2/RoofTop1"
# node = hou.node(nodePath)
# geo = node.geometry()

def main() :
    jsonDir = "D:/A_project/json_test"

    dir_template = {
        "Trivial":
            {
                "Type":
                    {
                        "VariableType": 19,
                        "Value": "UrbanEntity"
                    },
                "LocalToParentTransform":
                    {
                        "VariableType": 27,
                        "Transform":
                            {
                                "Translation": [2583, 470, 165],
                                "Rotation": [0, 0, 0],
                                "Scale": [1, 1, 1]
                            }
                    },
                "FriendlyName":
                    {
                        "VariableType": 24,
                        "Value": "UE_InstanceLayouter"
                    }
            },
        "SubPart":
            {
            },
    }
    nodePath = "/obj/UHA_Building_Body_Generator/UHA_Building_Body_Generator1/Roof/RoofTop_PC2/RoofTop1"
    repeatedList = []
    Node = {}

    node = hou.node(nodePath)
    geo = node.geometry()
    pt_list = geo.points()
    NodeList = []
    
    for pt in pt_list :
        pt_dir = {}
        sub_dir = {}
        element_count = pt.intAttribValue("element_count")
        element_name = pt.stringListAttribValue("element_name")
        element_pos = pt.floatListAttribValue("element_pos")
        element_rotate = pt.floatListAttribValue("element_rot")
        element_scale = pt.floatListAttribValue("element_scale")

        element_group = pt.stringAttribValue("group")
        fileName = os.path.join(jsonDir, element_group + ".json")

        for index in range(element_count) :
            current_name = element_name[index]
            current_p_x = element_pos[index * 3]
            current_p_y = element_pos[index * 3 + 1]
            current_p_z = element_pos[index * 3 + 2]

            current_r_x = element_rotate[index * 3]
            current_r_y = element_rotate[index * 3 + 1]
            current_r_z = element_rotate[index * 3 + 2]

            current_s_x = element_scale[index * 3]
            current_s_y = element_scale[index * 3 + 1]
            current_s_z = element_scale[index * 3 + 2]

            sub_dir["Type"] = {"VariableType" : 19, "Value" : "UrbanGeoNode"}
            sub_dir["LocalToParentTransform"] = {"VariableType" : 27, "Transform" : {"Translation" : [current_p_x, current_p_y, current_p_z], "Rotation" : [0, 0, 0], "Scale" : [1, 1, 1]}}
            sub_dir["FriendlyName"] = {"VariableType" : 24, "Value" : "Node"}
            sub_dir["unreal_instance"] = {"VariableType" : 24, "Value" : current_name}
            sub_dir["scale"] = {"VariableType" : 33, "Value" : [current_s_x, current_s_y, current_s_z]}
            sub_dir["rotate"] = {"VariableType" : 33, "Value" : [current_r_x, current_r_y, current_r_z]}
            
            pt_dir["Trivial"] = sub_dir
            pt_dir["SubPart"] = {}
            pt_dir["Repeated"] = []

            NodeList.append(pt_dir)
        Node["Node"] = NodeList
        repeatedList.append(Node)
        dir_template["Repeated"] = repeatedList

        result = json.dumps(dir_template, sort_keys = True, indent = 2)
        with open(fileName, "w+") as file :
            file.write(result)
