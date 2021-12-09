import json



node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.
inputNode = node.inputs()[0]
materialData = inputNode.parm("./mat_data").eval()

# print len(materialData)

# print 11532/1024
# print materialData

# print 11532 - 11*1024
textArray = []

for i in range(11532 / 1024):

    j = i * 1024
    k = j + 1023
    textArray.append(materialData[j:k])
    if i == 10:
        textArray.append(materialData[k + 1:])
text = "".join(textArray)
text = text.replace("\"{", "{")
text = text.replace("}\"", "}")
text = text.replace(r"\"", "\"")
text = text.replace(r"\r\n", "")
text = text.replace(r"\t", "")

prefabList = json.loads(text)

for prefab in prefabList:
    currentPrefab = prefab
    repeated = currentPrefab["Repeated"][0]["Part"]
    print repeated

    # currentWay = part["Trivial"]
    # point = geo.creatPoint()
    # for vName in currentWay :
    #     var = currentWay[vName]
    #     print var

