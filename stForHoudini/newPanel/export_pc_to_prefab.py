import hou

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
node = hou.node(nodePath)
geo = node.geometry()

def main() :
    nodePath = "/obj/UHA_Building_Body_Generator/UHA_Building_Body_Generator1/Roof/RoofTop_PC2/RoofTop1"

    node = hou.node(nodePath)
    geo = node.geometry()
    pt_list = geo.points()
    for pt in pt_list :



if __name__ == "__main__" :
    main()

