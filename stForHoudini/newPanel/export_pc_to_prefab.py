import os
import sys
import hou
import json
import pprint as pp

def getInstanceList(instance_path) :
    instance_list = []
    # in_path = "G:/51liuzhen/AES_V1_PaaS_Dev/Content/AssetRepository/model_library/prop/rooftop"
    in_path = instance_path
    for i in os.listdir(in_path) :
        current_path = os.path.join(in_path, i)
        if os.path.isfile(current_path) :
            instance_list.append(i.split(".")[0])
    return instance_list


def main() :

    inst_no_exists = []

    element_list = []

    in_path = "G:/51liuzhen/AES_V1_PaaS_Dev/Content/AssetRepository/model_library/prop/rooftop"
    instance_list = getInstanceList(in_path)
    # print len(instance_list)
    jsonDir = "G:/51liuzhen/prefab_json/v1_dev"
    hole_instance_dir = {}

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
            currentElementName = element_name[index].split("/")[-1].split(".")[0]
            if currentElementName not in hole_instance_dir:
                hole_instance_dir[currentElementName] = "SM_" + "_".join(currentElementName.split("_"))
                element_list.append(currentElementName)
            if currentElementName not in instance_list and currentElementName not in inst_no_exists:
                inst_no_exists.append(currentElementName)

            current_name = "DataAssetBuilding_L3/" + element_name[index].split("/")[-1].split(".")[0]

            current_p_x = element_pos[index * 3] * 100
            current_p_y = element_pos[index * 3 + 1] * 100
            current_p_z = element_pos[index * 3 + 2] * 100

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


            Node["Node"].append(pt_dir)
        repeatedList.append(Node)

        dir_template["Repeated"] = repeatedList


    # pp.pprint(hole_instance_dir)
    print len(hole_instance_dir)

    # pp.pprint(element_list)
    print "------------------------------"
    # pp.pprint(instance_list)
    pp.pprint(inst_no_exists)


def listCompare() :
    bb = []
    a = ['ac_unit_01','ac_unit_02','ac_unit_03','ac_unit_04','ac_unit_05','ac_unit_06','ac_unit_07','ac_unit_08','ac_unit_09','ac_unit_radiator','ac_unit_small_01','ac_unit_upright_01','AirDuct_Cap','airduct_split','AirDuct_Straight_Long', 'billboard','helipad' 'helipad_A_markings','pipe_double','pipe_front','pipe_underground','pipe_underground_01','pipe_underground_02','rooftops_platform','rooftop_vent','rooftop_vent_01','roof_ac_pipe_01','roof_antenna_01','roof_antenna_02','roof_antenna_large_01','roof_antenna_large_02','roof_antenna_large_03','roof_border','roof_bottom_exhaust','roof_breaker_box_01','roof_door','roof_exhaust_01','roof_exit_01','roof_exit_02','roof_exit_no_door_01','roof_exit_red_01','roof_exit_white_01','roof_ladder','roof_pipe_01','roof_pipe_exhaust_02','roof_pipe_metal_01','roof_pipe_metal_02','roof_pipe_metal_03','roof_pipe_metal_04','roof_pipe_metal_05','roof_pipe_metal_06','roof_pipe_metal_07','roof_pipe_metal_08','roof_pipe_metal_09','roof_pipe_metal_10','roof_platform_01','roof_platform_02','roof_platform_02_norailing','roof_platform_02_norailing_nolegs','roof_platform_02_norailing_short','roof_platform_stairs','roof_platform_turbine','roof_solar_panel_double','roof_stairs_platform','roof_stair_01','roof_stair_02','roof_stair_03','roof_stair_04','roof_stair_05','roof_stair_06','roof_storage','roof_storage_00','roof_storage_part','roof_track','roof_water_pipe_01','roof_window','roof_window_01','roof_window_02','turbine_engine']
    b = ['roof_window_01', 'rooftop_vent_01','roof_window_02','ac_unit_02','roof_solar_panel_double','roof_storage_00','roof_pipe_exhaust_02','airduct_Straight_shorts','AirDuct_Cap','AirDuct_90_Right','roof_storage','ac_unit_01','billboard','AirDuct_Straight_Long','ac_unit_06','roof_exit_01','AirDuct_90_Up','ac_unit_upright_01','pipe_front','roof_platform_02_norailing','ac_unit_small_01','rooftop_vent','roof_exit_02','roof_exit_no_door_01','AirDuct_Split','AirDuct_90_Left','roof_stair_06','ac_unit_09','ac_unit_03','roof_window','roof_platform_02','roof_antenna_02','pipe_underground','roof_storage_part','roof_antenna_large_01','ac_unit_07','roof_breaker_box_01','roof_exhaust_01','roof_antenna_01','roof_pipe_metal_03','helipad_A_markings','roof_stair_02','helipad','pipe_underground_02','turbine_engine','roof_ac_pipe_01','rooftops_platform','ac_unit_radiator','ac_unit_04','AirDuct_90_Down','ac_unit_08','roof_platform_02_norailing_nolegs','roof_exit_white_01','pipe_underground_01','roof_bottom_exhaust','roof_pipe_metal_01','roof_pipe_metal_08','roof_platform_01','roof_exit_red_01','roof_pipe_metal_09','roof_pipe_metal_02','roof_pipe_metal_07','roof_water_pipe_01','pipe_double','roof_antenna_large_02','roof_stair_05','roof_platform_02_norailing_short','roof_stairs_platform','roof_pipe_metal_06','roof_antenna_large_03','roof_platform_turbine','roof_platform_stairs','roof_pipe_01','roof_stair_04','roof_stair_03','roof_ladder','ac_unit_05','roof_door','roof_border']

    for i in b :
        if i not in a and i not in bb:
            bb.append(i)

    print bb




def checkDir() :
    sm_not_comfigure = {}
    sm_dir = {
            "ac_unit_01": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_01.SM_DistributionBox_01",
    "ac_unit_02": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_02.SM_DistributionBox_02",
    "ac_unit_03": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_03.SM_DistributionBox_03",
    "ac_unit_04": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_04.SM_DistributionBox_04",
    "ac_unit_05": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_05.SM_DistributionBox_05",
    "ac_unit_06": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_06.SM_DistributionBox_06",
    "ac_unit_07": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_07.SM_DistributionBox_07",
    "ac_unit_08": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_08.SM_DistributionBox_08",
    "ac_unit_09": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_DistributionBox_09.SM_DistributionBox_09",
    "ac_unit_radiator": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_Radiator_01.SM_Radiator_01",
    "ac_unit_small_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_SmallRadiator_01.SM_SmallRadiator_01",
    "ac_unit_upright_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_UprightRadiator_01.SM_UprightRadiator_01",
    "airduct_90_down": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_DownAirduct_01.SM_DownAirduct_01",
    "airduct_90_left": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_LeftAirduct_01.SM_LeftAirduct_01",
    "airduct_90_right": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RightAirduct_01.SM_RightAirduct_01",
    "airduct_90_up": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_UpAirduct_01.SM_UpAirduct_01",
    "airduct_cap": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_CapAirduct_01.SM_CapAirduct_01",
    "airduct_split": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_SplitAirduct_01.SM_SplitAirduct_01",
    "airduct_straight_long": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_LongAirduct_01.SM_LongAirduct_01",
    "airduct_straight_shorts": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_ShortsAirduct_01.SM_ShortsAirduct_01",
    "billboard": "StaticMesh /AesArtAsset/MeshLibrary/Prop/SM_Billboard_01.SM_Billboard_01",
    "helipad": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/helipad.helipad",
    "helipad_A_markings": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/helipad_A_markings.helipad_A_markings",
    "pipe_double": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_DoublePipe_01.SM_DoublePipe_01",
    "pipe_front": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_FrontPipe_01.SM_FrontPipe_01",
    "pipe_underground": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_UndergroundPipe_01.SM_UndergroundPipe_01",
    "pipe_underground_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_UndergroundPipe_02.SM_UndergroundPipe_02",
    "pipe_underground_02": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_UndergroundPipe_03.SM_UndergroundPipe_03",
    "roof_ac_pipe_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_Pipe_01.SM_Pipe_01",
    "roof_antenna_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofAntenna_01.SM_RoofAntenna_01",
    "roof_antenna_02": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofAntenna_02.SM_RoofAntenna_02",
    "roof_antenna_large_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofAntennaLarge_01.SM_RoofAntennaLarge_01",
    "roof_antenna_large_02": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofAntennaLarge_02.SM_RoofAntennaLarge_02",
    "roof_antenna_large_03": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofAntennaLarge_03.SM_RoofAntennaLarge_03",
    "roof_border": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofBorder_01.SM_RoofBorder_01",
    "roof_bottom_exhaust": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofBottomExhaust_01.SM_RoofBottomExhaust_01",
    "roof_breaker_box_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofBreakerBox_01.SM_RoofBreakerBox_01",
    "roof_door": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofDoor_01.SM_RoofDoor_01",
    "roof_exhaust_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofExhaust_01.SM_RoofExhaust_01",
    "roof_exit_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofExit_01.SM_RoofExit_01",
    "roof_exit_02": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofExit_02.SM_RoofExit_02",
    "roof_exit_no_door_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofExit_03.SM_RoofExit_03",
    "roof_exit_red_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofExit_04.SM_RoofExit_04",
    "roof_exit_white_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofExit_05.SM_RoofExit_05",
    "roof_ladder": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_Ladder_01.SM_Ladder_01",
    "roof_pipe_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipe_01.SM_RoofPipe_01",
    "roof_pipe_exhaust_02": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipe_02.SM_RoofPipe_02",
    "roof_pipe_metal_10": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_10.SM_RoofPipeMetal_10",
    "roof_pipe_metal_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_01.SM_RoofPipeMetal_01",
    "roof_pipe_metal_02": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_02.SM_RoofPipeMetal_02",
    "roof_pipe_metal_03": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_03.SM_RoofPipeMetal_03",
    "roof_pipe_metal_04": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_04.SM_RoofPipeMetal_04",
    "roof_pipe_metal_05": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_05.SM_RoofPipeMetal_05",
    "roof_pipe_metal_06": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_06.SM_RoofPipeMetal_06",
    "roof_pipe_metal_07": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_07.SM_RoofPipeMetal_07",
    "roof_pipe_metal_08": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_08.SM_RoofPipeMetal_08",
    "roof_pipe_metal_09": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPipeMetal_09.SM_RoofPipeMetal_09",
    "roof_platform_01": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_platform_01.roof_platform_01",
    "roof_platform_02": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_platform_02.roof_platform_02",
    "roof_platform_02_norailing": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_platform_02_norailing.roof_platform_02_norailing",
    "roof_platform_02_norailing_nolegs": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_platform_02_norailing_nolegs.roof_platform_02_norailing_nolegs",
    "roof_platform_02_norailing_short": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_platform_02_norailing_short.roof_platform_02_norailing_short",
    "roof_platform_stairs": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_platform_stairs.roof_platform_stairs",
    "roof_platform_turbine": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_platform_turbine.roof_platform_turbine",
    "roof_solar_panel_double": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_solar_panel_double.roof_solar_panel_double",
    "roof_stair_01": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_stair_01.roof_stair_01",
    "roof_stair_02": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_stair_02.roof_stair_02",
    "roof_stair_03": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_stair_03.roof_stair_03",
    "roof_stair_04": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_stair_04.roof_stair_04",
    "roof_stair_05": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_stair_05.roof_stair_05",
    "roof_stair_06": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_stair_06.roof_stair_06",
    "roof_stairs_platform": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_stairs_platform.roof_stairs_platform",
    "roof_storage": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofStorage_01.SM_RoofStorage_01",
    "roof_storage_00": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofStorage_02.SM_RoofStorage_02",
    "roof_storage_part": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_storage_part.roof_storage_part",
    "roof_track": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofTrack_01.SM_RoofTrack_01",
    "roof_water_pipe_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofWaterPipe_01.SM_RoofWaterPipe_01",
    "roof_window": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofWindow_01.SM_RoofWindow_01",
    "roof_window_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofWindow_02.SM_RoofWindow_02",
    "roof_window_02": "StaticMesh /Game/AssetRepository/model_library/prop/rooftop/roof_window_02.roof_window_02",
    "rooftop_vent": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RooftopVent_01.SM_RooftopVent_01",
    "rooftop_vent_01": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofTopVent_02.SM_RoofTopVent_02",
    "rooftops_platform": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_RoofPlatform_01.SM_RoofPlatform_01",
    "turbine_engine": "StaticMesh /AESArtAsset/AESArtAsset/MeshLibrary/Prop/SM_TurbineEngine_01.SM_TurbineEngine_01"
    }
    for i in sm_dir :
        currentPath = sm_dir[i]
        currentPath = currentPath.split(" ")[1]
        if(currentPath.startswith("/Game")) :
            sm_not_comfigure[i] = sm_dir[i]

    pp.pprint(sm_not_comfigure)
    name = "aaa.json"
    path = "C:/Users/liuzhen/Desktop/temp"
    fullJsonName = os.path.join(path, name)
    with open(fullJsonName, "w+") as file :
        file.write(json.dumps(sm_not_comfigure, sort_keys = 1, indent=2))



