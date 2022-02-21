import os
import sys
import hou
import json
import pprint as pp


# nodePath = "/obj/UHA_Building_Body_Generator/UHA_Building_Body_Generator1/Roof/RoofTop_PC2/RoofTop1"
# node = hou.node(nodePath)
# geo = node.geometry()
def main() :
    jsonDir = "G:/51liuzhen/prefab_json/v1_dev"

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
                                "Translation": [0, 0, 0],
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


    node = hou.node(nodePath)
    geo = node.geometry()
    pt_list = geo.points()
    
    for pt in pt_list :
        repeatedList = []
        Node = {}
        Node["Node"] = []

        element_count = pt.intAttribValue("element_count")
        element_name = pt.stringListAttribValue("element_name")
        element_pos = pt.floatListAttribValue("element_pos")
        element_rotate = pt.floatListAttribValue("element_rot")
        element_scale = pt.floatListAttribValue("element_scale")

        element_group = pt.stringAttribValue("group")
        fileName = os.path.join(jsonDir, element_group + ".json")

        for index in range(element_count) :
            sub_dir = {}
            pt_dir = {}
            current_name = "DataAssetBuilding_L3/" + element_name[index].split("/")[-1].split(".")[0]
            # current_name = element_name[index]
            current_p_x = element_pos[index * 3] * 100
            current_p_y = element_pos[index * 3 + 1] * 100
            current_p_z = element_pos[index * 3 + 2] * 100
            # if pt.number() == 3:
            #     print str(index) + " current postion : {}, {}, {}".format(current_p_x, current_p_y, current_p_z)

            current_r_x = element_rotate[index * 3]
            current_r_y = element_rotate[index * 3 + 2]
            current_r_z = element_rotate[index * 3 + 1]

            current_s_x = element_scale[index * 3]
            current_s_y = element_scale[index * 3 + 2]
            current_s_z = element_scale[index * 3 + 1]

            sub_dir["Type"] = {"VariableType" : 19, "Value" : "UrbanGeoNode"}
            sub_dir["LocalToParentTransform"] = {"VariableType" : 27, "Transform" : {"Translation" : [current_p_x, current_p_y, current_p_z], "Rotation" : [0, 0, 0], "Scale" : [1, 1, 1]}}
            sub_dir["FriendlyName"] = {"VariableType" : 24, "Value" : "Node"}
            sub_dir["unreal_instance"] = {"VariableType" : 24, "Value" : current_name}
            sub_dir["scale"] = {"VariableType" : 33, "Value" : [current_s_x, current_s_y, current_s_z]}
            sub_dir["rotate"] = {"VariableType" : 33, "Value" : [current_r_x, current_r_y, current_r_z]}

            pt_dir["Trivial"] = sub_dir


            pt_dir["SubPart"] = {}
            pt_dir["Repeated"] = []
            # if pt.number() == 3:
            #     pp.pprint(pt_dir)
            #     print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


            Node["Node"].append(pt_dir)
        repeatedList.append(Node)
        # if pt.number() == 3:
        #     print "-----------------------------------------------"
        #     pp.pprint(repeatedList)
        dir_template["Repeated"] = repeatedList
        # if pt.number() == 3 :
        #     pp.pprint(dir_template)

        result = json.dumps(dir_template, sort_keys = True, indent = 2)
        with open(fileName, "w+") as file :
            file.write(result)
