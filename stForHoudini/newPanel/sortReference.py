import hou


def fGetChildren() :
    validChildren = {}
    objNode = hou.node("/obj")
    objChildren = objNode.children()
    for i in objChildren :
        ccTypeList = [j.type().name() for j in i.children()]
        if "object_merge" in ccTypeList :
            # validChildren.append(i)
            validChildren[i.name()] = i
        else :
            if i.name() != "GlobalNodes":
                # validChildren.append(i)
                validChildren[i.name()] = i
    return validChildren


def getDep(currentNode) :

    deps = currentNode.dependents()
    print deps
    for dep in deps :
        getDep(dep)

def main():
    print "========================================================-=-=-=-=-=-="
    vChildren = fGetChildren()
    for child in vChildren :
        print "-------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        # print "dep : {} \n ref : {}".format(vChildren[child].dependents(), vChildren[child].references())
        if not vChildren[child].dependents()  :
            print "end : {}".format(child)

        elif not vChildren[child].references() :
            print "start : {}".format(child)
            getDep(vChildren[child])



