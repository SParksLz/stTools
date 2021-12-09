import s_core
reload(s_core)
import hou
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import hou

class customBar(QtWidgets.QProgressBar) :
    def __init__(self):
        super(customBar, self).__init__()
        # print "progress bar init"
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setFormat("%v")
        self.setStyleSheet("QProgressBar::chunk  {background-color: #CD96CD; border-radius :5px;}"
                           "QProgressBar {border: 1px solid grey;border-radius: 5px; text-align:center;}")


class progressItem(QtWidgets.QWidget) :
    def __init__(self, name, num, max):
        super(progressItem, self).__init__()
        self.name = name
        self.num = num
        self.max = max
        self.__mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.__mainLayout)

        self.__lable = QtWidgets.QLabel(name)
        self.__processBar = customBar()

        self.layout().addWidget(self.__lable)
        self.layout().addWidget(self.__processBar)

    def setBarRange(self):
        self.__processBar.setRange(0, self.max)

    def setBarValue(self):
        self.__processBar.setValue(self.num)



class progressList(QtWidgets.QListWidget) :
    def __init__(self):
        super(progressList, self).__init__()

    def addCustomItem(self, name, num, max):
        self.__customItem = progressItem(name, num, max)
        self.__customItem.setBarRange()
        self.__customItem.setBarValue()
        self.__itemFrame = QtWidgets.QListWidgetItem(self)

        self.__itemFrame.setSizeHint(QtCore.QSize(90, 34))
        self.setItemWidget(self.__itemFrame, self.__customItem)

    def add_items(self, array):
        if len(array) > 0 :
            maxNum = len(array[0].geometry().prims())
            for i in array :
                currentNum = len(i.geometry().prims())
                nodeName = i.name()
                self.addCustomItem(nodeName, currentNum, maxNum)


class nodeList(QtWidgets.QListWidget) :
    def __init__(self):
        super(nodeList, self).__init__()
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def add_items(self, array):
        for i in array :
            currentItem = self.addItem(i)



class listFrame(QtWidgets.QFrame):
    def __init__(self):
        super(listFrame, self).__init__()
        self._node_array = []
        self.__nodeLayout = QtWidgets.QVBoxLayout()
        self.__progressLayout = QtWidgets.QVBoxLayout()
        self.__mainLayout = QtWidgets.QHBoxLayout()

        self.__nodeList = nodeList()
        self.__progressList = progressList()


        self.__mainLayout.addLayout(self.__progressLayout)
        self.__mainLayout.addLayout(self.__nodeLayout)
        self.__progressLayout.addWidget(self.__progressList)
        self.__nodeLayout.addWidget(self.__nodeList)


        self.setAcceptDrops(True)
        self.setLayout(self.__mainLayout)


    def printHello(self):
        print "delete sth"

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        str_data = event.mimeData().data(hou.qt.mimeType.nodePath)
        if str_data :
            str_array = [str(s) for s in str_data.split("\t")]
            array_sorted = s_core.sortNodeList(str_array)
            if len(str_array) >= 0 :
                for i in str_array :
                    if i not in self._node_array :
                        self._node_array.append(i)
        self.update()
        event.acceptProposedAction()

    def keyPressEvent(self, event):
        currentKey = event.key()
        if currentKey == QtCore.Qt.Key_Delete :
            self.removeItem()
            self.update()

    def removeItem(self):
        items_selected = self.__nodeList.selectedItems()
        # print items_selected[0].text()
        # print self._node_array
        for item_s in items_selected :
            currentName = str(item_s.text())
            # print currentName
            self._node_array.remove(currentName)


    def update(self):
        self.__progressList.clear()
        self.__nodeList.clear()

        str_array = self._node_array
        array_sorted = s_core.sortNodeList(str_array)
        self.__progressList.add_items(array_sorted)
        self.__nodeList.add_items(str_array)

class mainWidget(QtWidgets.QWidget) :
    def __init__(self):
        super(mainWidget, self).__init__()
        self.__buildLayout()
        self.__buildListWidget()

    def __buildLayout(self):
        self.__testLable = QtWidgets.QLabel("Test")
        self.__mainLayout = QtWidgets.QVBoxLayout()
        self.__subLayout = QtWidgets.QHBoxLayout()

        self.setLayout(self.__mainLayout)
        self.__mainLayout.addWidget(self.__testLable)
        self.__mainLayout.addLayout(self.__subLayout)

    def __buildListWidget(self):
        self.__nodeFrame = listFrame()
        self.__subLayout.addWidget(self.__nodeFrame)






