from xml.dom.minidom import parseString


node = hou.pwd()
geo = node.geometry()

xmlString = node.evalParm("xmlString")

# Add code to modify contents of geo.
# Use drop down menu to select examples.

doc = parseString(xmlString)


collection = doc.documentElement
Info = collection.getElementsByTagName("object")


