import s_core
from PySide2 import QtWidgets


class mainWidget(QtWidgets.QWidget) :
    def __init__(self):
        super(mainWidget, self).__init__()
        self.__buildLayout()
        self.__addButton()

    def __buildLayout(self):
        self.__mainLayout = QtWidgets.QHBoxLayout()
        self.__subLayout_r = QtWidgets.QVBoxLayout()
        self.__subLayout_l = QtWidgets.QVBoxLayout()

        self.setLayout(self.__mainLayout)
        self.__mainLayout.addLayout(self.__subLayout_l)
        self.__mainLayout.addLayout(self.__subLayout_r)


    def __addButton(self):
        self.__button_a = QtWidgets.QPushButton("a")
        self.__button_b = QtWidgets.QPushButton("b")

        self.__subLayout_r.addWidget(self.__button_a)
        self.__subLayout_l.addWidget(self.__button_b)



