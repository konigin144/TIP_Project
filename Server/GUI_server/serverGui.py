import sys, path, os, asyncio, threading 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QApplication

from serverGuiFunc import *
from serverStylesheets import *
import server 

class Ui_Dialog(object):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(600, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        Dialog.setStyleSheet(dialogStyle)
        Dialog.setFixedSize(Dialog.size())
        Dialog.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        Dialog.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        Dialog.setWindowIcon(QIcon(self.imgPath + "window_icon.png"))

        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 581, 781))
        self.layoutWidget.setObjectName("layoutWidget")
       
        self.contentLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setObjectName("contentLayout")
        
        self.roomsDropDown = QtWidgets.QComboBox(self.layoutWidget)
        self.roomsDropDown.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.roomsDropDown.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.roomsDropDown.setStyleSheet(roomsDropDownStyle)
        self.roomsDropDown.setEditable(False)
        self.roomsDropDown.setObjectName("roomsDropDown")
        self.roomsDropDown.addItem("General info")
        self.roomsDropDown.setMaxVisibleItems(11)
        self.roomsDropDown.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.roomsDropDown.view().setCursor(QCursor(QtCore.Qt.PointingHandCursor)) # Set pointer to the content of dropdown  
        self.contentLayout.addWidget(self.roomsDropDown)
        
        self.scrollBar = QtWidgets.QScrollBar()
        self.scrollBar.setStyleSheet(scrollBarStyle)

        self.logsArea = QtWidgets.QTextBrowser(self.layoutWidget)
        self.logsArea.setStyleSheet(logsAreaStyle)
        self.logsArea.setObjectName("logsArea")
        self.logsArea.setVerticalScrollBar(self.scrollBar)
        self.contentLayout.addWidget(self.logsArea)
        
        self.bottomLayout = QtWidgets.QFormLayout()
        self.bottomLayout.setObjectName("bottomLayout")
        
        self.inputsLayout = QtWidgets.QGridLayout()
        self.inputsLayout.setObjectName("inputsLayout")
        
        self.ipLayout = QtWidgets.QFormLayout()
        self.ipLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.ipLayout.setObjectName("ipLayout")
        
        self.ipLabel = QtWidgets.QLabel(self.layoutWidget)
        self.ipLabel.setMinimumSize(QtCore.QSize(45, 20))
        self.ipLabel.setMaximumSize(QtCore.QSize(45, 20))
        self.ipLabel.setStyleSheet(ipLabelStyle)
        self.ipLabel.setObjectName("ipLabel")
        self.ipLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ipLabel)
        
        self.ipInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.ipInput.setMinimumSize(QtCore.QSize(150, 20))
        self.ipInput.setMaximumSize(QtCore.QSize(150, 20))
        self.ipInput.setToolTip("")
        self.ipInput.setStyleSheet(ipInputStyle)
        self.ipInput.setObjectName("ipInput")
        self.ipLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ipInput)
        self.inputsLayout.addLayout(self.ipLayout, 0, 0, 1, 1)
 
        self.portLayout = QtWidgets.QFormLayout()
        self.portLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.portLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.portLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.portLayout.setObjectName("portLayout")
        
        self.portLabel = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portLabel.sizePolicy().hasHeightForWidth())
        self.portLabel.setSizePolicy(sizePolicy)
        self.portLabel.setMinimumSize(QtCore.QSize(45, 20))
        self.portLabel.setMaximumSize(QtCore.QSize(45, 20))
        self.portLabel.setStyleSheet(portLabelStyle)
        self.portLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.portLabel.setOpenExternalLinks(False)
        self.portLabel.setObjectName("portLabel")
        self.portLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.portLabel)
        
        self.portInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.portInput.setMinimumSize(QtCore.QSize(150, 20))
        self.portInput.setMaximumSize(QtCore.QSize(150, 20))
        self.portInput.setStyleSheet(portInputStyle)
        self.portInput.setObjectName("portInput")
        self.portLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.portInput)
        self.inputsLayout.addLayout(self.portLayout, 1, 0, 1, 1)
        
        self.bottomLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.inputsLayout)
        self.btnLayout = QtWidgets.QGridLayout()
        self.btnLayout.setObjectName("btnLayout")
        
        self.startBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.startBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) #hover effect
        self.startBtn.setMinimumSize(QtCore.QSize(100, 30))
        self.startBtn.setMaximumSize(QtCore.QSize(100, 30))
        self.startBtn.setStyleSheet(startBtnStartStyle)
        self.startBtn.setObjectName("startBtn")
        self.btnLayout.addWidget(self.startBtn, 0, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.bottomLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.btnLayout)
        self.contentLayout.addLayout(self.bottomLayout)
   
        self.startBtn.setCheckable(True) 

        #methods mapping
        Ui_Dialog.startTh = startTh
        Ui_Dialog.stopTh = stopTh
        Ui_Dialog.updateLogs = updateLogs
        Ui_Dialog.checkInputs = checkInputs
        Ui_Dialog.checkIp = checkIp
        Ui_Dialog.checkPort = checkPort
        Ui_Dialog.checkSocket = checkSocket
        Ui_Dialog.handleClick = handleClick
        Ui_Dialog.checkNumOfRooms = checkNumOfRooms 
        Ui_Dialog.fillDropdown = fillDropdown
        Ui_Dialog.clearDropdown = clearDropdown
        Ui_Dialog.handleItemDropdown = handleItemDropdown
        Ui_Dialog.addLogs = addLogs

        self.threadList = []
        self.portList = []
        self.logsDict = {'general': []}
        self.currentLog = 'general'
        self.isActive = False
        self.startBtn.clicked.connect(self.handleClick)
        self.roomsDropDown.activated[str].connect(self.handleItemDropdown)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.roomsList = ["General info"]

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Server"))
        self.ipLabel.setText(_translate("Dialog", "IP:"))
        self.portLabel.setText(_translate("Dialog", "Rooms:"))
        self.startBtn.setText(_translate("Dialog", "START"))

import res_rc

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
