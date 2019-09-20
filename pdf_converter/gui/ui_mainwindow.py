# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pdfConverterDesign3.4.ui',
# licensing of 'pdfConverterDesign3.4.ui' applies.
#
# Created: Fri Sep 13 12:05:07 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.openFileLayout = QtWidgets.QHBoxLayout()
        self.openFileLayout.setObjectName("openFileLayout")
        self.openFolderButton = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openFolderButton.setIcon(icon)
        self.openFolderButton.setIconSize(QtCore.QSize(50, 50))
        self.openFolderButton.setObjectName("openFolderButton")
        self.openFileLayout.addWidget(self.openFolderButton)
        self.openFileButton = QtWidgets.QToolButton(self.centralwidget)
        self.openFileButton.setEnabled(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openFileButton.setIcon(icon1)
        self.openFileButton.setIconSize(QtCore.QSize(50, 50))
        self.openFileButton.setObjectName("openFileButton")
        self.openFileLayout.addWidget(self.openFileButton)
        self.gridLayout_2.addLayout(self.openFileLayout, 0, 0, 1, 1)
        self.testLayout = QtWidgets.QVBoxLayout()
        self.testLayout.setObjectName("testLayout")
        self.testButton = QtWidgets.QToolButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../icons/testing.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.testButton.setIcon(icon2)
        self.testButton.setIconSize(QtCore.QSize(50, 50))
        self.testButton.setObjectName("testButton")
        self.testLayout.addWidget(self.testButton)
        self.gridLayout_2.addLayout(self.testLayout, 0, 2, 1, 1)
        self.toolButtonLayout = QtWidgets.QHBoxLayout()
        self.toolButtonLayout.setObjectName("toolButtonLayout")
        self.splitButton = QtWidgets.QToolButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../icons/split.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.splitButton.setIcon(icon3)
        self.splitButton.setIconSize(QtCore.QSize(50, 50))
        self.splitButton.setObjectName("splitButton")
        self.toolButtonLayout.addWidget(self.splitButton)
        self.changePositionOfPicButton = QtWidgets.QToolButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../icons/swap.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changePositionOfPicButton.setIcon(icon4)
        self.changePositionOfPicButton.setIconSize(QtCore.QSize(50, 50))
        self.changePositionOfPicButton.setObjectName("swapButton")
        self.toolButtonLayout.addWidget(self.changePositionOfPicButton)
        self.rotateButton = QtWidgets.QToolButton(self.centralwidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../icons/rotate.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateButton.setIcon(icon5)
        self.rotateButton.setIconSize(QtCore.QSize(50, 50))
        self.rotateButton.setObjectName("rotateButton")
        self.toolButtonLayout.addWidget(self.rotateButton)
        self.cropButton = QtWidgets.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../icons/crop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cropButton.setIcon(icon6)
        self.cropButton.setIconSize(QtCore.QSize(50, 50))
        self.cropButton.setObjectName("cropButton")
        self.toolButtonLayout.addWidget(self.cropButton)
        self.trashButton = QtWidgets.QToolButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../icons/trash.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trashButton.setIcon(icon7)
        self.trashButton.setIconSize(QtCore.QSize(50, 50))
        self.trashButton.setObjectName("trashButton")
        self.toolButtonLayout.addWidget(self.trashButton)
        self.gridLayout_2.addLayout(self.toolButtonLayout, 3, 1, 1, 1)
        self.widgetLayout = QtWidgets.QWidget(self.centralwidget)
        self.widgetLayout.setObjectName("widgetLayout")
        self.picButtonLayout = QtWidgets.QHBoxLayout(self.widgetLayout)
        self.picButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.picButtonLayout.setObjectName("picButtonLayout")
        self.leftButton = QtWidgets.QToolButton(self.widgetLayout)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../icons/arrowleft.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftButton.setIcon(icon8)
        self.leftButton.setIconSize(QtCore.QSize(50, 50))
        self.leftButton.setObjectName("leftButton")
        self.picButtonLayout.addWidget(self.leftButton)
        self.pushButtonGrid = QtWidgets.QGridLayout()
        self.pushButtonGrid.setObjectName("pushButtonGrid")
        self.picButtonLayout.addLayout(self.pushButtonGrid)
        self.rightButton = QtWidgets.QToolButton(self.widgetLayout)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("../icons/arrowright.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rightButton.setIcon(icon9)
        self.rightButton.setIconSize(QtCore.QSize(50, 50))
        self.rightButton.setObjectName("rightButton")
        self.picButtonLayout.addWidget(self.rightButton)
        self.gridLayout_2.addWidget(self.widgetLayout, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.actionOpen_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addAction(self.actionOpen_File)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.openFolderButton.setText(QtWidgets.QApplication.translate("MainWindow", "Open Folder", None, -1))
        self.openFileButton.setText(QtWidgets.QApplication.translate("MainWindow", "Open File", None, -1))
        self.splitButton.setText(QtWidgets.QApplication.translate("MainWindow", "Split", None, -1))
        self.changePositionOfPicButton.setText(QtWidgets.QApplication.translate("MainWindow", "swap", None, -1))
        self.rotateButton.setText(QtWidgets.QApplication.translate("MainWindow", "rotate", None, -1))
        self.cropButton.setText(QtWidgets.QApplication.translate("MainWindow", "cropping", None, -1))
        self.trashButton.setText(QtWidgets.QApplication.translate("MainWindow", "trash", None, -1))
        self.leftButton.setText(QtWidgets.QApplication.translate("MainWindow", "arrowleft", None, -1))
        self.rightButton.setText(QtWidgets.QApplication.translate("MainWindow", "arrowright", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.actionOpen_Folder.setText(QtWidgets.QApplication.translate("MainWindow", "Open Folder", None, -1))
        self.actionOpen_File.setText(QtWidgets.QApplication.translate("MainWindow", "Open File", None, -1))
