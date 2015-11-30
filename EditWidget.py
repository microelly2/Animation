# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
from PySide import QtCore, QtGui

class _EditWidget(QtGui.QWidget):
	'''double clicked dialog''' 
	def __init__(self, dialer,obj,menu,*args):
		QtGui.QWidget.__init__(self, *args)
		obj.widget=self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.vollabel = QtGui.QLabel(obj.Object.Label)

		if dialer:
			dial = QtGui.QDial()
			dial.setNotchesVisible(True)
			self.dial=dial
			dial.setMaximum(100)
			dial.valueChanged.connect(obj.dialer);

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.vollabel)

		for m in menu:
			bt=QtGui.QPushButton(m[0])
			bt.clicked.connect(m[1])
			layout.addWidget(bt)

		if dialer:
			layout.addWidget(dial)

		self.pushButton02 = QtGui.QPushButton("close")
		self.pushButton02.clicked.connect(self.hide)
		layout.addWidget(self.pushButton02)

		self.setLayout(layout)
		try:
			self.setWindowTitle(obj.Object.target.Label)
		except:
			pass


class EditWidget(_EditWidget):
	def __init__(self, obj,menu,*args):
		_EditWidget.__init__(self, True, obj,menu,*args)

class EditNoDialWidget(_EditWidget):
	def __init__(self, obj,menu,*args):
		_EditWidget.__init__(self, False, obj,menu,*args)
