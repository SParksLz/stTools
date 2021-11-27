import s_core
import hou
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


class progressList(QtWidgets.QListWidget) :
    def __init__(self):
        super(progressList, self).__init__()



class nodeList(QtWidgets.QListWidget) :
    def __init__(self):
        super(nodeList, self).__init__()

class listFrame(QtWidgets.QFrame):
    def __init__(self):
        super(listFrame, self).__init__()
        self._node_array = []
        self.__nodeLayout = QtWidgets.QVBoxLayout()
        self.__progressLayout = QtWidgets.QVBoxLayout()
        self.__mainLayout = QtWidgets.QHBoxLayout()

        self.__nodeList = QtWidgets.QListWidget()
        self.__progressList = QtWidgets.QListWidget()



        self.__mainLayout.addLayout(self.__progressLayout)
        self.__mainLayout.addLayout(self.__nodeLayout)
        self.__progressLayout.addWidget(self.__progressList)
        self.__nodeLayout.addWidget(self.__nodeList)

        self.setAcceptDrops(True)
        self.setLayout(self.__mainLayout)


    def __addItem(self, data):
        self.__progressList.addItem(data)

        self.__nodeList.addItem(data)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        str = event.mimeData().data(hou.qt.mimeType.nodePath)
        if str :
            str_array = str.split("\t")
            if len(str_array) >= 0 :
                for i in str_array :
                    if i not in self._node_array :
                        self._node_array.append(i)
                        self.__addItem("{}".format(i))
                    # self.addItem(i)
        # str_array = str.split("\t")
        # self.addItem(str)


        event.acceptProposedAction()










class mainWidget(QtWidgets.QWidget) :
    def __init__(self):
        super(mainWidget, self).__init__()
        self.__buildLayout()
        self.__buildListWidget()

    def __buildLayout(self):
        self.__testLable = QtWidgets.QLabel("Test")
        self.__mainLayout = QtWidgets.QVBoxLayout()
        self.__subLayout = QtWidgets.QHBoxLayout()
        self.__subLayout_r = QtWidgets.QVBoxLayout()
        self.__subLayout_l = QtWidgets.QVBoxLayout()

        self.setLayout(self.__mainLayout)
        self.__mainLayout.addWidget(self.__testLable)
        self.__mainLayout.addLayout(self.__subLayout)
        self.__subLayout.addLayout(self.__subLayout_l)
        self.__subLayout.addLayout(self.__subLayout_r)


    def __buildListWidget(self):
        self.__pbList = progressList()
        self.__nodeList = nodeList()
        self.__aaa = listFrame()
        self.__subLayout_l.addWidget(self.__pbList)
        self.__subLayout_r.addWidget(self.__nodeList)
        self.__subLayout_r.addWidget(self.__aaa)






