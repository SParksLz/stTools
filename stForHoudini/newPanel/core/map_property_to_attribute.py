import json

node = hou.pwd()
geo = node.geometry()
parentNode = hou.parent()

# Add code to modify contents of geo.
# Use drop down menu to select examples.

prefabData = parentNode.parm("prefab_data").eval()


textArray = []
step = len(prefabData) / 1024
for i in range(step):

    j = i * 1024
    k = j + 1023
    textArray.append(prefabData[j:k])
    if i == step - 1:
        textArray.append(prefabData[k + 1:])

text = "".join(textArray)
text = text.replace("\"{", "{")
text = text.replace("}\"", "}")
text = text.replace(r"\"", "\"")
text = text.replace(r"\r\n", "")
text = text.replace(r"\t", "")


prefabList = json.loads(text)


for prefab in prefabList:
    currentPrefab = prefab
    repeated = currentPrefab["Repeated"][0]["Part"][0]

    currentWay = repeated["Trivial"]

    point = geo.createPoint()
    for vName in currentWay:
        varDir = currentWay[vName]
        valueType = varDir["VariableType"]
        value = 0
        if "Value" in varDir:
            if valueType == 10 :
                varDir["Value"] = float(varDir["Value"])
            elif valueType == 17 :
                varDir["Value"] = hou.Vector4(varDir["Value"][0], varDir["Value"][1], varDir["Value"][2], varDir["Value"][3])
            value = varDir["Value"]
            if not geo.findPointAttrib(vName) :
                geo.addAttrib(point.attribType(), vName, value)
            point.setAttribValue(vName, value)


        # print "{} : type : {} -----value : {}".format(vName, valueType, value)