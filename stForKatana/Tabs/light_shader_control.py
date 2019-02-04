import sys
import os
from Katana import QtGui, QtCore
from Katana import NodegraphAPI, Utils, Nodes3DAPI
from UI4.Tabs import BaseTab
import UI4.App as ua
import UI4.FormMaster.PythonValuePolicy
from UI4.Widgets.SceneGraphView import SceneGraphTree
from Katana import FnGeolib
from Katana import ScenegraphManager
from PackageSuperToolAPI import UIDelegate



class Light_shader_control(BaseTab):
    def __init__(self, parent=None):
        UI4.Tabs.BaseTab.__init__(self, parent)
        self._header = ['Name', 'Light type', 'Location']
        self.buildUI()


    def buildUI(self):
        self._topgroup = QtGui.QGroupBox(self)
        self._topgroup.setLayout(QtGui.QVBoxLayout())
        self._topgroup.setTitle('Lights')

        #Lights list
        self._lightlist = QtGui.QListWidget()
        self._lightlist.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


        #Checkbox & PushButton
        self._Select = QtGui.QCheckBox('Select')
        self._LookThrough = QtGui.QCheckBox('Look Through')
        self._refreshbutton = QtGui.QPushButton('Refresh')
        self._testbutton = QtGui.QPushButton('test')


        self._insidegroup = QtGui.QGroupBox(self)
        self._insidegroup.setLayout(QtGui.QHBoxLayout())
        self._insidegroup.layout().addWidget(self._Select)
        self._insidegroup.layout().addWidget(self._LookThrough)
        self._insidegroup.layout().addWidget(self._refreshbutton)
        self._insidegroup.layout().addWidget(self._testbutton)

        self._topgroup.layout().addWidget(self._lightlist)
        self._topgroup.layout().addWidget(self._insidegroup)


        self.scrollWidget = QtGui.QWidget(self)
        self.scrollWidget.setObjectName('scrollWidget')
        self.scrollLayout = QtGui.QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setObjectName('scrollLayout')
        self.scrollLayout.setSpacing(2)
        self.scrollLayout.setMargin(2)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setObjectName('scrollArea')
        self.scrollArea.setFrameStyle(QtGui.QFrame.NoFrame + QtGui.QFrame.Plain)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)

        self.vBoxlayout = QtGui.QVBoxLayout()
        self.vBoxlayout.addWidget(self._topgroup)
        self.vBoxlayout.addWidget(self.scrollArea)
        self.setLayout(self.vBoxlayout)
        self._refreshbutton.clicked.connect(self.refresh)
        self._testbutton.clicked.connect(lambda v : self.change_listvalue(self._lightlist.selectedItems()))

    def refresh(self):
        self._lightlist.clear()
        all_light_shader = []
        list_item = []
        all_material = NodegraphAPI.GetAllNodesByType('Material')
        all_edit_mat = [x for x in all_material if x.getParameter('action').getValue(0) == 'edit material']
        for mat in all_edit_mat:
            if mat.getParameter('shaders.arnoldLightShader.value') is not None and mat.getParameter('shaders.arnoldLightShader.value').getValue(0) != 'skydome_light':
                all_light_shader.append(mat.getParameter('edit.location').getValue(0))

        for light_shader in all_light_shader:
            self._lightlist.addItem(light_shader)
        self._lightlist.itemSelectionChanged.connect(self.itemselected)

    def itemselected(self):
        client = self.getClient(NodegraphAPI.GetAllSelectedNodes()[0])
        activeSc = ScenegraphManager.getActiveScenegraph()
        activeSc.clearSelection(sender=None)
        select_list = self._lightlist.selectedItems()
        if len(select_list) == 1 :
            if self._LookThrough.checkState() == 2 :
                a = ua.Tabs.FindTopTab("Viewer")
                a.setLookThrough(str(self._lightlist.currentItem().text()), frameId=0)
            if self._Select.checkState() == 2 :
            # activeSc.clearSelection(sender=None)
                activeSc.setLocationSelected(str(select_list[0].text()))
            # self.parameterUpdate_gui()
            material = self.getMaterialnode(client, str(self._lightlist.currentItem().text()))
            lightnode = self.getLightnode(client, str(self._lightlist.currentItem().text()))
            self.get_parameter(material, lightnode)
        elif len(select_list) > 1 :
            if self._Select.checkState() == 2 :
                for selection in select_list :
                    activeSc.setLocationSelected(str(selection.text()))
            self.parameterUpdate_gui()

    def getClient(self, node):
        """
        return the node client Op
        """
        runtime = FnGeolib.GetRegisteredRuntimeInstance()
        txn = runtime.createTransaction()
    
        # get the op naturally generated from this node
        op1 = Nodes3DAPI.GetOp(txn, node, NodegraphAPI.GetCurrentGraphState())
    
        # create a client through which to query the output of an op
        client = txn.createClient()
        txn.setClientOp(client, op1)
        runtime.commit(txn)
        return client

    def getMaterialnode(self, client, loc):
        location = client.cookLocation(str(loc))
        attr = location.getAttrs()
        a = attr.getChildByName('attributeEditor')
        node = a.getChildByName('exclusiveTo')
        nodefromscene = NodegraphAPI.GetNode(node.getValue())
        parent = nodefromscene.getParent()
        mat_list = []
        for i in parent.getChildren():
            if i.getType() == 'Material':
                mat_list.append(i)
        return mat_list[0]

    def getLightnode(self, client, loc):
        location = client.cookLocation(str(loc))
        attr = location.getAttrs()
        a = attr.getChildByName('attributeEditor')
        node = a.getChildByName('exclusiveTo')
        nodefromscene = NodegraphAPI.GetNode(node.getValue())
        return nodefromscene

    def get_parameter(self, node, lightnode):
        self.clearLayout(self.scrollLayout)

        color = node.getParameter('shaders.arnoldLightParams.color')
        intersity = node.getParameter('shaders.arnoldLightParams.intensity')
        exposure = node.getParameter('shaders.arnoldLightParams.exposure')
        spread = node.getParameter('shaders.arnoldLightParams.spread')
        roundness = node.getParameter('shaders.arnoldLightParams.roundness')
        soft_edge = node.getParameter('shaders.arnoldLightParams.soft_edge')
        sample = node.getParameter('shaders.arnoldLightParams.samples')
        aov = node.getParameter('shaders.arnoldLightParams.aov')
        diffuse = node.getParameter('shaders.arnoldLightParams.diffuse')
        specular = node.getParameter('shaders.arnoldLightParams.specular')
        sss = node.getParameter('shaders.arnoldLightParams.sss')
        indirect = node.getParameter('shaders.arnoldLightParams.indirect')
        volume = node.getParameter('shaders.arnoldLightParams.volume')
        scale = lightnode.getParameter('transform.scale')
        myGroupPolicyData = {
            '__childOrder': ['color',
                             'intensity',
                             'exposure',
                             'spread',
                             'roundness',
                             'soft_edge',
                             'samples',
                             'aov',
                             'diffuse',
                             'specular',
                             'sss',
                             'indirect',
                             'volume',
                             'scale'],
        }
        group_policy = UI4.FormMaster.PythonValuePolicy.PythonValuePolicy('Control', myGroupPolicyData)
        if color is not None:
            color_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, color)
            group_policy.addChildPolicy(color_parameterpolicy)
        if intersity is not None:
            intersity_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, intersity)
            group_policy.addChildPolicy(intersity_parameterpolicy)
        if exposure is not None:
            exposure_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, exposure)
            group_policy.addChildPolicy(exposure_parameterpolicy)
        if spread is not None:
            spread_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, spread)
            group_policy.addChildPolicy(spread_parameterpolicy)
        if roundness is not None:
            roundness_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, roundness)
            group_policy.addChildPolicy(roundness_parameterpolicy)
        if soft_edge is not None:
            soft_edge_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, soft_edge)
            group_policy.addChildPolicy(soft_edge_parameterpolicy)
        if sample is not None:
            sample_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, sample)
            group_policy.addChildPolicy(sample_parameterpolicy)
        if diffuse is not None:
            diffuse_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, diffuse)
            group_policy.addChildPolicy(diffuse_parameterpolicy)
        if specular is not None:
            specular_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, specular)
            group_policy.addChildPolicy(specular_parameterpolicy)
        if sss is not None:
            sss_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, sss)
            group_policy.addChildPolicy(sss_parameterpolicy)
        if indirect is not None:
            indirect_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, indirect)
            group_policy.addChildPolicy(indirect_parameterpolicy)
        if volume is not None:
            volume_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, volume)
            group_policy.addChildPolicy(volume_parameterpolicy)
        if aov is not None:
            aov_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, aov)
            group_policy.addChildPolicy(aov_parameterpolicy)
        scale_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, scale)
        group_policy.addChildPolicy(scale_parameterpolicy)
        # print dir(group_policy)

        group_widget = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory.buildWidget(None, group_policy)
        self.scrollLayout.addWidget(group_widget)
        self.scrollLayout.addStretch()

    def parameterUpdate_gui(self):
        self.clearLayout(self.scrollLayout)

        self.colors_group = self.color_widget()
        self.intensity = self.slider_widget('Intensity')
        self.int_linee = self.intensity.children()[2]
        self.int_slider = self.intensity.children()[3]
        self.int_slider.valueChanged.connect(lambda v: self.int_linee.setText(str(self.int_slider.value())))
        self.int_linee.textChanged.connect(lambda v: self.int_slider.setValue(int(self.int_linee.text())))
        self.int_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'intensity',float(self.int_linee.text())))

        self.exposure = self.slider_widget('Exporsure')
        self.exp_linee = self.exposure.children()[2]
        self.exp_slider = self.exposure.children()[3]
        self.exp_slider.valueChanged.connect(lambda v: self.exp_linee.setText(str(self.exp_slider.value())))
        self.exp_linee.textChanged.connect(lambda v: self.exp_slider.setValue(int(self.exp_linee.text())))
        self.exp_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'exposure',float(self.exp_linee.text())))

        self.sample = self.slider_widget('Sample')
        self.samp_linee = self.sample.children()[2]
        self.samp_slider = self.sample.children()[3]
        self.samp_slider.valueChanged.connect(lambda v: self.samp_linee.setText(str(self.samp_slider.value())))
        self.samp_linee.textChanged.connect(lambda v: self.samp_slider.setValue(int(self.samp_linee.text())))
        self.samp_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'samples',float(self.samp_linee.text())))

        self.diffuse = self.slider_widget('Diffuse')
        self.dif_linee = self.diffuse.children()[2]
        self.dif_slider = self.diffuse.children()[3]
        self.dif_slider.valueChanged.connect(lambda v: self.dif_linee.setText(str(self.dif_slider.value())))
        self.dif_linee.textChanged.connect(lambda v: self.dif_slider.setValue(int(self.dif_linee.text())))
        self.dif_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'diffuse',float(self.dif_linee.text())))

        self.specular = self.slider_widget('Specular')
        self.spe_linee = self.specular.children()[2]
        self.spe_slider = self.specular.children()[3]
        self.spe_slider.valueChanged.connect(lambda v: self.spe_linee.setText(str(self.spe_slider.value())))
        self.spe_linee.textChanged.connect(lambda v: self.spe_slider.setValue(int(self.spe_linee.text())))
        self.spe_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'specular',float(self.spe_linee.text())))

        self.sss = self.slider_widget('SSS')
        self.sss_linee = self.sss.children()[2]
        self.sss_slider = self.sss.children()[3]
        self.sss_slider.valueChanged.connect(lambda v: self.sss_linee.setText(str(self.sss_slider.value())))
        self.sss_linee.textChanged.connect(lambda v: self.sss_slider.setValue(int(self.sss_linee.text())))
        self.sss_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'sss',float(self.sss_linee.text())))

        self.indirect = self.slider_widget('Indirect')
        self.ind_linee = self.indirect.children()[2]
        self.ind_slider = self.indirect.children()[3]
        self.ind_slider.valueChanged.connect(lambda v: self.ind_linee.setText(str(self.ind_slider.value())))
        self.ind_linee.textChanged.connect(lambda v: self.ind_slider.setValue(int(self.ind_linee.text())))
        self.ind_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'indirect',float(self.ind_linee.text())))

        self.volume = self.slider_widget('Volume')
        self.vol_linee = self.volume.children()[2]
        self.vol_slider = self.volume.children()[3]
        self.vol_slider.valueChanged.connect(lambda v: self.vol_linee.setText(str(self.vol_slider.value())))
        self.vol_linee.textChanged.connect(lambda v: self.vol_slider.setValue(int(self.vol_linee.text())))
        self.vol_linee.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'volume',float(self.vol_linee.text())))

        self.aov = QtGui.QLineEdit('default')
        self.aov.textChanged.connect(lambda v: self.change_listvalue(self._lightlist.selectedItems(), 'aov',str(self.aov.text())))
        self.aov_label = QtGui.QLabel('aov')
        self._aovgroup = QtGui.QGroupBox()
        self._aovgroup.setLayout(QtGui.QHBoxLayout())
        self._aovgroup.layout().addWidget(self.aov_label)
        self._aovgroup.layout().addWidget(self.aov)


        self.scrollLayout.addWidget(self.color_group)
        self.scrollLayout.addWidget(self.intensity)
        self.scrollLayout.addWidget(self.exposure)
        self.scrollLayout.addWidget(self.sample)
        self.scrollLayout.addWidget(self.diffuse)
        self.scrollLayout.addWidget(self.specular)
        self.scrollLayout.addWidget(self.sss)
        self.scrollLayout.addWidget(self.indirect)
        self.scrollLayout.addWidget(self.volume)
        self.scrollLayout.addWidget(self._aovgroup)
        self.scrollLayout.addStretch()

    def itemselected(self):
        client = self.getClient(NodegraphAPI.GetAllSelectedNodes()[0])
        activeSc = ScenegraphManager.getActiveScenegraph()
        activeSc.clearSelection(sender=None)
        select_list = self._lightlist.selectedItems()
        if len(select_list) == 1 :
            if self._LookThrough.checkState() == 2 :
                a = ua.Tabs.FindTopTab("Viewer")
                a.setLookThrough(str(self._lightlist.currentItem().text()), frameId=0)
            if self._Select.checkState() == 2 :
            # activeSc.clearSelection(sender=None)
                activeSc.setLocationSelected(str(select_list[0].text()))
            # self.parameterUpdate_gui()
            material = self.getMaterialnode(client, str(self._lightlist.currentItem().text()))
            lightnode = self.getLightnode(client, str(self._lightlist.currentItem().text()))
            self.get_parameter(material, lightnode)
        elif len(select_list) > 1 :
            if self._Select.checkState() == 2 :
                for selection in select_list :
                    activeSc.setLocationSelected(str(selection.text()))
            self.parameterUpdate_gui()

    '''@test.'''
    def get_current_text(self):
        name = ''
        if self._lightlist.currentItem() is not None:
            name = '%s' % (self._lightlist.currentItem().text())
        return name

    def test(self, text):


        print 'clicked!'+text

    def asd(self):


        print 'asdasd'

    def clearLayout(self, layout):
        if layout is not None :
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None :
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def build(self):
        self.pythonValuePolicy = UI4.FormMaster.PythonValuePolicy.PythonValuePolicy(
                'Control',
                {   'Common'    :{'Color'          : [1.0, 1.0, 1.0],
                                  'Intensity'      : 1.0,
                                  'Exposure'       : 0.0,
                                  'Spread'         : 1.0,
                                  'Roundness'      : 0.0,
                                  'Soft_Edge'      : 0.0,
                                  'Sample'         : 1,
                                  'volume_samples' : 2,
                                  'aov'            : 'default',
                                  '__childOrder' : ['Color',
                                                    'Intensity',
                                                    'Exposure',
                                                    'Spread',
                                                    'Roundness',
                                                    'Soft_Edge',
                                                    'Sample',
                                                    'Volume_samples',
                                                    'AOV',],
                                  '__childHints' : {
                                                      'Color'     : {'widget'   : 'color' ,
                                                                     'color_enableFilmlookVis'          : True,
                                                                     'color_enableNoFilmlookColorSpace' : True,
                                                                     'color_restrictComponents'         : True},
                                                      'Intensity' : {'widget'   : 'number',
                                                                     'min'      : 0.0,
                                                                     'slider'   : True,
                                                                     'slidermin': 0.0,
                                                                     'slidermax': 10.0,},
              
                                                      'Exposure'  : {'widget'   : 'number',
                                                                     'slider'   : True,
                                                                     'slidermin': -100.0,
                                                                     'slidermax': 100.0,},
              
                                                      'Spread'    : {'widget'   : 'number',
                                                                     'min'      : 0.0,
                                                                     'max'      : 1.0,
                                                                     'slider'   : True,
                                                                     'slidermin': 0.0,
                                                                     'slidermax': 1.0,},
              
                                                      'Roundness' : {'widget'   : 'number',
                                                                     'min'      : 0.0,
                                                                     'max'      : 1.0,
                                                                     'slider'   : True,
                                                                     'slidermin': 0.0,
                                                                     'slidermax': 1.0,},
              
                                                      'Soft_Edge' : {'widget'   : 'number',
                                                                     'min'      : 0.0 ,
                                                                     'max'      : 1.0 ,
                                                                     'slider'   : True ,
                                                                     'slidermin': 0.0 ,
                                                                     'slidermax': 1.0,},
              
                                                      'Sample'    : {'widget'   : 'number',
                                                                     'min'      : 1,
                                                                     'max'      : 100,
                                                                     'int'      : True,
                                                                     'slider'   : True,
                                                                     'slidermin': 0,
                                                                     'slidermax': 96,},
                                                      'Volume_samples':{'widget' : 'number',},
                                                   },},

                })
        groupFormWidget = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory.buildWidget(None, self.pythonValuePolicy)
        self.scrollLayout.addWidget(groupFormWidget)
        self.ccolor = self.pythonValuePolicy.getChildByName('Common').getChildByName('Color')
        self.iintensity = self.pythonValuePolicy.getChildByName('Common').getChildByName('Intensity')
        print groupFormWidget

    def color_widget(self):
        self.color_group = QtGui.QGroupBox()
        self.color_group = QtGui.QGroupBox()
        self.color_group.setLayout(QtGui.QHBoxLayout())
        self.color_label = QtGui.QLabel('Color')
        self.color_label.setMinimumWidth(60)
        self.color_button = QtGui.QPushButton()
        self.color_r = QtGui.QLineEdit()
        self.color_g = QtGui.QLineEdit()
        self.color_b = QtGui.QLineEdit()
        # self.color_button.setStyleSheet('QPushButton{border: None}')
        self.color_group.layout().addWidget(self.color_label)
        self.color_group.layout().addWidget(self.color_button)
        self.color_group.layout().addStretch()
        self.color_dialog = QtGui.QColorDialog()
        self.color_button.clicked.connect(lambda v: self.color_dialog.open())
        # self.printxxx(self.color_dialog.getColor().name())
        # self.color_button.setStyleSheet('QWidget{background-color:rgb(0,0,0)}')
        self.color_dialog.currentColorChanged.connect(lambda v: self.color_button.setStyleSheet('QWidget{background-color:%s}' % (self.color_dialog.currentColor().name())))
        return self.color_group

    def slider_widget(self, name):
        self._label = QtGui.QLabel(name)
        self._label.setMinimumWidth(60)
        self._groupbox = QtGui.QGroupBox()
        self._groupbox.setLayout(QtGui.QHBoxLayout())
        self._lineedit = QtGui.QLineEdit()
        self._lineedit.setMaximumWidth(50)
        self._slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        # self._slider.valueChanged.connect(lineedit_change())
        # self._lineedit.editingFinished.connect(slider_change())
        self._groupbox.layout().addWidget(self._label)
        # self._groupbox.layout().addStretch()
        self._groupbox.layout().addWidget(self._lineedit)
        self._groupbox.layout().addWidget(self._slider)

        # def lineedit_change():
        #     self._lineedit.setText(str(self._slider.value()))
        # def slider_change():
        #     self._slider.setValue(int(self._lineedit.text()))
        # self._slider.valueChanged.connect(lineedit_change())
        # self._lineedit.editingFinished.connect(slider_change())
        return self._groupbox

    def change_listvalue(self, iterlist, name, value):
        client = self.getClient(NodegraphAPI.GetAllSelectedNodes()[0])
        itermlist = iterlist
        locationlist = [iterm.text() for iterm in itermlist]
        matlist = [self.getMaterialnode(client, location) for location in locationlist]
        for mat in matlist:
            if mat.getParameter('shaders.arnoldLightParams.%s.enable' % (name)).getValue(0) == 0.0:
                mat.getParameter('shaders.arnoldLightParams.%s.enable' % (name)).setValue(1.0, 0)

            mat.getParameter('shaders.arnoldLightParams.%s.value' % (name)).setValue(value, 0)

PluginRegistry = [
                    ("KatanaPanel", 2.0, "X/Light_shader_control",Light_shader_control)
                 ]