import os
import json

node = hou.pwd()
geo = node.geometry()
fileName = node.evalParm("filePath")
basefileName = os.path.basename(fileName)
dirname = os.path.dirname(fileName)
newName = basefileName.split(".")[0] + "_Export.json"

newFilePath = dirname + "/" + newName

ii_attr = geo.stringListAttribValue("instance_info")


def mergeJson(file, newData, mode=0):
    """
    @param file:    当mode=0时为文件路径,mode=1时则接收的是一个json对象
    @param newData: 接收的是一个被合并的json对象
    @param mode:    默认为0,主要用来更改接收的file的对象类型
    @return:
    """
    jsonObj = None
    new_data = None

    if mode == 0:
        with open(file) as f:
            # print(type(f))
            jsonObj = json.load(f)

    elif mode == 1:
        jsonObj = file

    new_data = json.loads(newData)
    roads = jsonObj["roads"]
    new_road_array = []
    for road in roads:

        roadId = road["roadId"]
        # print(roadId)
        if str(roadId) in new_data:
            instance_info_array = new_data[str(roadId)]
            # road["RoadPiers"] = instance_info_array
            for instance in instance_info_array:
                instance_type = instance["instance_type"]
                if instance_type not in road:
                    road[instance_type] = []
                    road[instance_type].append(instance)
                else:
                    road[instance_type].append(instance)
            new_road_array.append(road)
        else:
            new_road_array.append(road)
    jsonObj["roads"] = new_road_array
    return jsonObj


with open(newFilePath, "w", encoding='utf-8') as f:
    m = mergeJson(fileName, ii_attr[0])
    m = mergeJson(m, ii_attr[1], mode=1)
    json.dump(m, f, indent=2, sort_keys=True, ensure_ascii=False)
