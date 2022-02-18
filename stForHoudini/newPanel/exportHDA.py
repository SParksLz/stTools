import hou
import os
import subprocess

dirName = "G:\\51liuzhen\\AES_V1_PaaS_dev\\hda"
unpackdir = dirName + "\\unpacked_version"
otlPath = "C:\\Program Files\\Side Effects Software\\Houdini 18.0.416\\bin\\hotl.exe"

def exportHDA() :
    hdaList = []
    objNode = hou.node("/obj")
    childrenNode = objNode.children()
    for i in childrenNode :
        if i.name() != "GlobalNodes" and i.name() != "null" :
            currentChildren = i.children()
            for child in currentChildren :
                if child.type().name() != "object_merge" :
                    hdaList.append(child)

    for hda in hdaList :
        hdaDef = hda.type().definition()
        libPath = hdaDef.libraryFilePath()
        # newName = nameConvertion[hda.type().name()]
        print libPath

        oriName = hda.type().name()
        oriList = oriName.split("_")
        if oriList[0] == "udb" or oriList[0] == "hda" or oriList[0] == "Udb" or oriList[0] == "ubd" or oriList[0] == "Ubd":
            oriList[0] = "UHA"
        elif oriList[0]:
            pass
        else :
            oriList.insert(0, "UHA")

        if "::" in oriList[-1] :
            oriList[-1] = oriList[-1].split("::")[0]

        newList = [i[0].upper()+i[1:] for i in oriList]
        newMenuList = [i.lower() for i in oriList]

        newName = "_".join(newList)
        newMenuName = " ".join(newMenuList)
        if newName.endswith("1"):
            newName = newName[:-1]
        if newMenuName.endswith("1"):
            newMenuName = newMenuName[:-1]

        # print newName
        # print newMenuName
        hda.allowEditingOfContents()

        hdaFilePath = dirName + "\\{}.hda".format(newName)
        unpackFilePath = unpackdir + "\\{}.hda".format(newName)
        # print hdaFilePath
        # print unpackFilePath
        hdaDef.copyToHDAFile(hdaFilePath, newName, newMenuName)
        cmd = "{} -t {} {}".format(otlPath, unpackFilePath, hdaFilePath)
        print cmd
        subprocess.call(cmd)




        # print os.path.exists(libPath)
        # hda.allowEditingOfContents()
        # if libPath == "Embedded" or os.path.exists(libPath) == False :
        #     print hda.name()
        #     hda.allowEditingOfContents()




