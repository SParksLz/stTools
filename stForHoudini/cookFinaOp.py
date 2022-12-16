import os
import sys
import hou


def cook_name(hip_file, json_file, save_hip=False):
    # load(file_name, suppress_save_prompt=False, ignore_load_warnings=False)

    hip_file_name = os.path.basename(hip_file)
    hip_dir_name = os.path.dirname(hip_file)

    json_file_name = os.path.basename(json_file).split(".")[0]
    json_dir_name = os.path.dirname(json_file)
    hou.hipFile.load(hip_file, ignore_load_warnings=True)

    od_loader_node = hou.node("/obj/geo1/SimOne_OD_Loader1")
    file_parm = od_loader_node.parm("filePath")
    file_parm.set(json_file)


    if save_hip is True :
        hou.hipFile.save(os.path.join(hip_dir_name, "/debug/{0}.hip".format(json_file_name)))

    current_node = hou.node("/obj/geo1/simone_od_exporter2/output0")
    current_node.cook()
    # print(current_node)

if __name__ == "__main__":
    hipFile = sys.argv[1]
    jsonFile = sys.argv[2]
    cook_name(hipFile, jsonFile)
