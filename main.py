import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem ,QWidget, QHBoxLayout ,QFileDialog, QComboBox, QPushButton, QLineEdit, QLabel, QScrollArea
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from ContactQuality import ContactQuality
from cortex import *
import time
import numpy as np
import pandas as pd
import _thread
import os
from database import *
#from main3D import *
from random import shuffle

class OpenPage(QWidget):
    def __init__(self):
        super().__init__()
        # First of all elements of the GUI are created, positioned and so on..
        # 

        # Section of defining general settings
        self.setGeometry(300, 300, 1200, 800)
        self.setFixedHeight(800)
        self.setFixedWidth(1200)
        self.setWindowTitle("BCI - Machine Control through EEG - Welcome Page")

        self.background = QLabel(self)
        self.background.setGeometry(-360, -40, 1751, 841)
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("Visuals/background1.png"))
        self.background.setObjectName("background")

        self.ListWidget = QListWidget(self)
        self.ListWidget.setGeometry(650, 340, 521, 251)
        #self.ListWidget.setWidgetResizable(False)
        self.ListWidget.setObjectName("ListWidget")

        # Section of defining the buttons to navigate
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(1040, 730, 121, 31)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Next Page")

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(90, 420, 113, 32)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Select")

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 580, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Delete")

        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(90, 350, 113, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("Create")

        self.pushButton_5 = QPushButton(self)
        self.pushButton_5.setGeometry(650, 610, 113, 32)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText("Add File")

        self.pushButton_6 = QPushButton(self)
        self.pushButton_6.setGeometry(770, 610, 113, 32)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setText("Delete File")

        # Section of defining Combo Boxes for selecting and deleting of profiles
        self.OptionMenu_1 = QComboBox(self)
        self.OptionMenu_1.setGeometry(220, 420, 321, 32)
        self.OptionMenu_1.setObjectName("OptionMenu_1")
        self.OptionMenu_1.setItemText(0, "Select Profile")

        self.OptionMenu_2 = QComboBox(self)
        self.OptionMenu_2.setGeometry(220, 580, 321, 32)
        self.OptionMenu_2.setObjectName("OptionMenu_2")
        self.OptionMenu_2.setItemText(0,"Delete Profile")

        #Section of defining Lines for creating profiles
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(220, 350, 301, 31)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        # Section for defining labels with text for a better overview and understanding
        font = QtGui.QFont()
        font.setPointSize(25)

        self.label_1 = QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(100, 260, 461, 91))
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_1.setText("Please create a profile or select an exisiting profile")


        self.label_2 = QLabel(self)
        self.label_2.setGeometry(100, 490, 461, 91)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Please select one of the following profiles \nif you want to delete it")


        self.label_3 = QLabel(self)
        self.label_3.setGeometry(890, 270, 461, 91)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Current files for selection")

        # Section for adding functionality to created buttons, lines and so on
        self.initialize_OptionMenu()
        self.pushButton_6.clicked.connect(self.delete_ListWidget)
        self.pushButton_5.clicked.connect(self.update_ListWidget)
        self.pushButton_4.clicked.connect(self.update_OptionMenu)
        self.pushButton_3.clicked.connect(self.delete_OptionMenu)
        self.pushButton_2.clicked.connect(self.initialize_ListWidget)
        self.pushButton.clicked.connect(self.new_window)
        self.update_OptionMenu()

        self.show()

    # After each starting we need to keep consistent relations between GUI and database
    # Also applying changes in GUI or database always need an update
    # i.e. Removing a profile means, also removing it from the database and also update GUI visualizsations
    # otherwise it can be still possible to see the deleted profile in 'Select profile'

    def initialize_ListWidget(self):
        files = show_entries('Files')
        profile = self.OptionMenu_1.currentText()
        self.ListWidget.clear()
        for file in files:
            if file[0] == profile:
                print(file)
                item = QListWidgetItem(file[2])
                self.ListWidget.addItem(item)


    def update_ListWidget(self):
        options = QFileDialog.Options()
        profile = self.OptionMenu_1.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;CSV Files (*.csv)",
                                    options=options)
        full_path = filename
        file_name = filename.split("/")

        print("Following injection")
        print(file_name)
        add_file_to_db(file_name[5], full_path, profile)
        self.initialize_ListWidget()


    def delete_ListWidget(self):
        file = self.ListWidget.currentItem()
        print(file.text())
        delete_file_from_db(file.text(), "Files")
        self.initialize_ListWidget()


    def initialize_OptionMenu(self):
        profiles = show_entries('Profiles')
        self.OptionMenu_1.clear()
        self.OptionMenu_2.clear()

        for profile in profiles:
            self.OptionMenu_1.addItem(profile)
            self.OptionMenu_2.addItem(profile)

        #self.OptionMenu_1.currentIndexChanged.connect(self.clicked)


    def delete_OptionMenu(self):
        name = self.OptionMenu_2.currentText()
        if name != "":
            print(name)
            delete_profile_from_db(name)
            #self.OptionMenu_1.currentIndexChanged.connect(self.clicked)
            self.initialize_OptionMenu()


    def update_OptionMenu(self):
        name = self.lineEdit.text()
        if name != "":
            self.lineEdit.clear()
            add_profile_to_db(name)
            self.initialize_OptionMenu()

    # Used to switch between windows and keeping track of the position when opening a new windows
    def new_window(self):
        name = self.OptionMenu_1.currentText()
        if name != '':
            pos = self.pos()
            self.CQ = ContactQuality(name, self, pos)
            self.CQ.show()
            self.hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OpenPage()
    sys.exit(app.exec_())
