import sys, path, os, asyncio, threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import QSize

from clientGuiFunc import *
from clientStylesheets import *
import client 

class Ui_Dialog(object):
    imgPath = os.path.dirname(os.path.abspath(__file__)) + "/images/"
    def setupUi(self, Dialog):
        Dialog.setObjectName("Client")
        Dialog.setEnabled(True)
        Dialog.resize(341, 210)
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

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(12, 12, 316, 115))
        self.widget.setObjectName("widget")

        self.upperLayout = QtWidgets.QGridLayout(self.widget)
        self.upperLayout.setContentsMargins(0, 0, 0, 0)
        self.upperLayout.setObjectName("upperLayout")

        self.inputsLayout = QtWidgets.QFormLayout()
        self.inputsLayout.setObjectName("inputsLayout")

        self.ipLayout = QtWidgets.QFormLayout()
        self.ipLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.ipLayout.setObjectName("ipLayout")

        self.ipLabel = QtWidgets.QLabel(self.widget)
        self.ipLabel.setMinimumSize(QtCore.QSize(40, 20))
        self.ipLabel.setMaximumSize(QtCore.QSize(40, 20))
        self.ipLabel.setStyleSheet(ipLabelStyle)
        self.ipLabel.setObjectName("ipLabel")
        self.ipLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ipLabel)
        
        self.ipInput = QtWidgets.QLineEdit(self.widget)
        self.ipInput.setMinimumSize(QtCore.QSize(150, 20))
        self.ipInput.setMaximumSize(QtCore.QSize(150, 20))
        self.ipInput.setToolTip("")
        self.ipInput.setStyleSheet(ipInputStyle)
        self.ipInput.setObjectName("ipInput")
        self.ipLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ipInput)
        self.inputsLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.ipLayout)

        self.portLayout = QtWidgets.QFormLayout()
        self.portLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.portLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.portLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.portLayout.setObjectName("portLayout")
        
        self.portLabel = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portLabel.sizePolicy().hasHeightForWidth())
        self.portLabel.setSizePolicy(sizePolicy)
        self.portLabel.setMinimumSize(QtCore.QSize(40, 20))
        self.portLabel.setMaximumSize(QtCore.QSize(40, 20))
        self.portLabel.setStyleSheet(portLabelStyle)
        self.portLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.portLabel.setOpenExternalLinks(False)
        self.portLabel.setObjectName("portLabel")
        self.portLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.portLabel)
        
        self.portInput = QtWidgets.QLineEdit(self.widget)
        self.portInput.setMinimumSize(QtCore.QSize(150, 20))
        self.portInput.setMaximumSize(QtCore.QSize(150, 20))
        self.portInput.setStyleSheet(portInputStyle)
        self.portInput.setObjectName("portInput")
        self.portLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.portInput)
        self.inputsLayout.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.portLayout)

        self.nickLayout = QtWidgets.QFormLayout()
        self.nickLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.nickLayout.setObjectName("nickLayout")
        
        self.nickLabel = QtWidgets.QLabel(self.widget)
        self.nickLabel.setMinimumSize(QtCore.QSize(40, 20))
        self.nickLabel.setMaximumSize(QtCore.QSize(40, 20))
        self.nickLabel.setStyleSheet(nickLabelStyle)
        self.nickLabel.setObjectName("nickLabel")
        self.nickLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nickLabel)
        
        self.nickInput = QtWidgets.QLineEdit(self.widget)
        self.nickInput.setMinimumSize(QtCore.QSize(150, 20))
        self.nickInput.setMaximumSize(QtCore.QSize(150, 20))
        self.nickInput.setToolTip("")
        self.nickInput.setStyleSheet(nickInputLabel)
        self.nickInput.setObjectName("nickInput")
        self.nickLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nickInput)
        self.inputsLayout.setLayout(2, QtWidgets.QFormLayout.LabelRole, self.nickLayout)
        self.upperLayout.addLayout(self.inputsLayout, 1, 0, 1, 1)
        
        self.startBtnLayout = QtWidgets.QGridLayout()
        self.startBtnLayout.setObjectName("startBtnLayout")
        self.startBtn = QtWidgets.QPushButton(self.widget)
        self.startBtn.setMinimumSize(QtCore.QSize(100, 30))
        self.startBtn.setMaximumSize(QtCore.QSize(100, 30))
        self.startBtn.setStyleSheet(startBtnStartStyle)
        self.startBtn.setObjectName("startBtn")
        self.startBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.startBtnLayout.addWidget(self.startBtn, 0, 0, 1, 1)
        self.upperLayout.addLayout(self.startBtnLayout, 1, 1, 1, 1)
        
        self.statusBar = QtWidgets.QComboBox(self.widget)
        self.statusBar.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.statusBar.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.statusBar.setStyleSheet(statusBarStyle)
        self.statusBar.setEditable(False)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.addItem("Please insert below parameters - start port is 29200.")
        self.statusBar.setMaxVisibleItems(11)
        self.statusBar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.upperLayout.addWidget(self.statusBar, 0, 0, 1, 2)
        
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(40, 140, 181, 53))
        self.widget1.setObjectName("widget1")
        
        self.gridBtn = QtWidgets.QGridLayout(self.widget1)
        self.gridBtn.setContentsMargins(0, 0, 0, 0)
        self.gridBtn.setObjectName("gridBtn")
        
        self.spkBtn = QtWidgets.QPushButton(self.widget1)
        self.spkBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.spkBtn.setMinimumSize(QtCore.QSize(50, 50))
        self.spkBtn.setMaximumSize(QtCore.QSize(50, 50))
        self.spkBtn.setIcon(QIcon(self.imgPath + "speaker_on.png"))
        self.spkBtn.setIconSize(QSize(30, 30))
        self.spkBtn.setStyleSheet(spkBtnStyle)
        self.spkBtn.setText("")
        self.spkBtn.setObjectName("spkBtn")
        self.gridBtn.addWidget(self.spkBtn, 0, 1, 1, 1)
        
        self.micBtn = QtWidgets.QPushButton(self.widget1)
        self.micBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.micBtn.setMinimumSize(QtCore.QSize(50, 50))
        self.micBtn.setMaximumSize(QtCore.QSize(50, 50))
        self.micBtn.setIcon(QIcon(self.imgPath + "mic_on.png"))
        self.micBtn.setIconSize(QSize(30, 30))
        self.micBtn.setStyleSheet(micBtnStyle)
        self.micBtn.setText("")
        self.micBtn.setObjectName("micBtn")
        self.gridBtn.addWidget(self.micBtn, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.startBtn.setCheckable(True) 

        #methods mapping
        Ui_Dialog.startTh = startTh
        Ui_Dialog.stopTh = stopTh
        Ui_Dialog.checkInputs = checkInputs
        Ui_Dialog.checkIp = checkIp
        Ui_Dialog.checkPort = checkPort
        Ui_Dialog.updateStatus = updateStatus
        Ui_Dialog.checkSocket = checkSocket
        Ui_Dialog.initClient = initClient
        Ui_Dialog.handleClickStartBtn = handleClickStartBtn
        Ui_Dialog.handleMicroBtn = handleMicroBtn
        Ui_Dialog.handleSpeakerBtn = handleSpeakerBtn
        Ui_Dialog.startBtnChangeStatus = startBtnChangeStatus
        Ui_Dialog.fillDropdown = fillDropdown
        Ui_Dialog.checkNick = checkNick
        Ui_Dialog.preventDropdownChange = preventDropdownChange
        
        self.thread = None
        self.isActive = False
        self.muteMicFlag = False
        self.muteSpkFlag = False
        self.startBtn.clicked.connect(self.handleClickStartBtn)
        self.micBtn.clicked.connect(self.handleMicroBtn)
        self.spkBtn.clicked.connect(self.handleSpeakerBtn)
        self.statusBar.currentIndexChanged.connect(self.preventDropdownChange)

        self.usersList = ["Please insert below parameters - start port is 29200."]

        self.initClient()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Client"))
        self.ipLabel.setText(_translate("Dialog", "IP:"))
        self.portLabel.setText(_translate("Dialog", "Port:"))
        self.nickLabel.setText(_translate("Dialog", "Nick:"))
        self.startBtn.setText(_translate("Dialog", "CONNECT"))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
