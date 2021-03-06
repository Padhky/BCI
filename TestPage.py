# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

#from Asynchron import connect, Live_data, disconnect
from PyQt5.QtWidgets import QApplication, QProgressBar, QListWidgetItem ,QWidget, QHBoxLayout ,QFileDialog, QComboBox, QPushButton, QLineEdit, QLabel, QScrollArea, QSpinBox
from PyQt5 import QtCore, QtGui, QtWidgets
from random import shuffle
from main3D import *
import _thread
from cortex import *
from datetime import date as d
from Model_with_hyperparameter import Model
import pandas as pd
import glob
from joblib import load, dump
from queue import Queue, Empty
from threading import Thread, Lock

class TestPage(QWidget):
    def __init__(self, name, parent, pos):
        super().__init__()

        # Section for general settings
        self.name = name
        print(self.name)
        self.parent = parent
        self.move(pos)

        """create folder for new user"""
        file = manage_file()
        self.folder = file.make_dir(self.name)  # create a folder for  each user
        self.overlap = 0.75                     # Overlap window used for live mode
        self.prediction = Queue()               # Append a predicition in live mode
        self.di = []                            
        self.count = 0                          # Counter to update the progress bar in TestPage of GUI
        self.to_append_marker = []
        self.train_count = 0                    # Interlock for exporting the file

        '''Replace your license, client id, and client secret here'''
        user = {
            "license": "6212ad8d-9046-48a9-ae2f-6d8f2ed9945d",
            'client_id': 'FqBZUgxeajUkiNwhRaTmRiUcSHRmwl42PneVbNh1',
            'client_secret': 'FXQj2Arp7Uw28eAbnWkUG1SBzqWAu5hY2pNpRZDIsqkvBCZFobj5voPAvGH0YrEAC0cx1CasxLwepJ9lKXDVY3qCAagD4DNCugxk29aUjehvSaTYBef3jLycrPf5Tmqz',
            "debit": 100
        }

        ############## defining Model or load model if there is
        try:
            self.model = load(f'{self.folder}\\{self.name}.joblib')
            print('Model Found!')
            self.count =  self.model.training

        except FileNotFoundError:
            print("Not found")
            self.model = Model(self.name)
            print("model created")


        self.cortex = Cortex(user, True)
        

        self.resize(892, 633)
        self.setFixedHeight(633)
        self.setFixedWidth(892)
        self.setWindowTitle("BCI - Machine Control through EEG - Test Page")

        self.background = QLabel(self)
        self.background.setGeometry(-680, -10, 1671, 711)

        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("Visuals/background1.png"))
        self.background.setObjectName("background")

        self.background = QLabel(self)
        self.background.setGeometry(290, 130, 595, 371)

        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("Visuals/trainbrain.jpg"))
        self.background.setObjectName("inside background")

        """Display number of training"""
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(150, 330, 85, 25)
        self.pbar.setValue(self.count)
        self.pbar.setStyleSheet("QProgressBar")
        self.pbar.setFormat(str(self.count))


        self.pbar1 = QProgressBar(self)
        self.pbar1.setGeometry(150, 260, 85, 25)
        self.pbar1.setValue(self.count)
        self.pbar1.setStyleSheet("QProgressBar")
        self.pbar1.setFormat(str(self.count))


        self.pbar2 = QProgressBar(self)
        self.pbar2.setGeometry(150, 400, 85, 25)
        self.pbar2.setValue(self.count)
        self.pbar2.setStyleSheet("QProgressBar")
        self.pbar2.setFormat(str(self.count))

        self.pbar3 = QProgressBar(self)
        self.pbar3.setGeometry(150, 190, 85, 25)
        self.pbar3.setValue(self.count)
        self.pbar3.setStyleSheet("QProgressBar")
        self.pbar3.setFormat(str(self.count))


        # Section for progress bars which indicate training progress
        # and their corresponding labels

        self.label_6 = QLabel(self)
        self.label_6.setGeometry(50, 330, 71, 31)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("Neutral")

        self.label_7 = QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(50, 260, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("Forward")

        self.label_8 = QLabel(self)
        self.label_8.setGeometry(50, 400, 71, 31)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_8.setText("Stop")

        self.label_9 = QLabel(self)
        self.label_9.setGeometry(50, 190, 71, 31)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_9.setText("Rotate")

    
        # Section for adding buttons to navigate
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(610, 570, 113, 32)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Train Mode")

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(730, 570, 113, 32)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Live Mode")

        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(50, 570, 113, 32)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Back")


        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setGeometry(300, 570, 113, 32)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("Finish")

        # Section for adding functionality to the buttons
        #self.pushButton_4.clicked.connect(lambda: self.stop_Live)
        self.pushButton.clicked.connect(self.start_Training)
        self.pushButton_2.clicked.connect(lambda: self.start_Live(True))
        self.pushButton_3.clicked.connect(self.move_back)
        self.pushButton_4.clicked.connect(self.end_recording)


    def start_Training(self):

        """Create a session and record the raw EEG data"""

        if self.train_count == 0:
            self.cortex.do_prepare_steps()
            t = time.localtime()
            current_time = time.strftime("%H_%M_%S", t)
            self.EEG_file_name = 'EEG_' + str(self.name) + '_' + str(current_time) + '_' + str(d.today())
            self.cortex.create_record(self.EEG_file_name, 'EEG_test')
            self.train_count +=1
        self.start_sequence_test()


    def move_back(self):
        pos = self.pos()
        self.parent.move(pos)
        self.parent.show()
        self.close()

    def start_sequence_test(self):
        neutral_marker = {"Label": "Neutral", "Value": 0}
        forward_marker = {"Label": "Forward", "Value": 1}
        rotate_marker = {"Label": "Rotate", "Value": 2}
        stop_marker = {"Label": "Stop", "Value": 3}

        order = [neutral_marker, forward_marker, rotate_marker, stop_marker]
        shuffle(order) # shuffle the order of cues
        # Parameter for start_3Danimation is the speed of Rotation, values around 0.005 are normal
        Cube = start_3Danimation(0.001)
        # Labels are: 'Rotate', 'Forward', 'Neutral', 'Stop'
        for direction in order:
            mark = marker(direction["Value"])
            #self.cortex.inject_marker_request(mark)
            Cube.run_test(True, direction)
        time.sleep(0.5)
        self.count = self.count + 1
        self.model.training = self.count   # Update the count in model.py
        """Append all the marker start and end value for the entire training
            Cube.marker_csv can be accessed in main3D.py
        """
        self.to_append_marker.append(Cube.marker_csv) 
        quit_3Danimation()

        """Update the progress bar in TestPage"""
        self.pbar.setValue(self.count)
        self.pbar.setFormat(str(self.count))
        self.pbar1.setValue(self.count)
        self.pbar1.setFormat(str(self.count))
        self.pbar2.setValue(self.count)
        self.pbar2.setFormat(str(self.count))
        self.pbar3.setValue(self.count)
        self.pbar3.setFormat(str(self.count))



    def end_recording(self):
        """Once Finish button pressed in TestPage:
        1. Export EEG file and updated marker file
        2. Read those files and process feature extraction, Dimensionality Reduction and classification using model_with_hyperparameter.py

         """

        self.count = 0
        marker_file_data = [e for sl in self.to_append_marker for e in sl]
        data_marker = pd.DataFrame(marker_file_data, columns=('Start', 'End', 'Label', 'Value'))
        t = time.localtime()
        current_time = time.strftime("%H_%M_%S", t)
        file_name = 'MARKERS_' + str(self.name) + '_' + str(current_time) + '_' + str(d.today())
        data_marker.to_csv(f'{self.folder}\\{file_name}.csv', index=False)
        self.marker_path = f'{self.folder}\\{file_name}.csv'
        #Feature Extraction
        self.create_EEG_file()
        """Train Model"""
        self.model.extract_features(self.eeg_path, self.marker_path)
        """ Hyper parameter"""
        hyperparameter = self.model.hyperparameter(self.eeg_path, self.marker_path)

        self.model.train(hyperparameter)
        #store joblib file to use it whenever user logs in again
        with open(f'{self.folder}\\{self.name}.joblib', 'wb') as fo:
            dump(self.model, fo)


    def create_EEG_file(self):
        """Export the EEG file to the user folder"""

        self.cortex.stop_record()
        self.cortex.disconnect_headset()
        folder = self.folder
        export_format = 'CSV'
        export_types = ['EEG']
        export_version = "V2"
        record_ids = [self.cortex.record_id]

        self.cortex.export_record(folder,
                             export_types,
                             export_format,
                             export_version,
                             record_ids)

        path = f'{self.folder}\\{self.EEG_file_name}*.csv'
        for file in glob.glob(path):
            self.eeg_path = file
        print(self.eeg_path)


    def live_prediction(self):
        """stop recording, export files and train the model"""
        self.cortex.do_prepare_steps()
        self.cortex.sub_request(['eeg'])
        self.cortex.get_data()
        f_s = 128 #sampling rate
        window_size = 3*f_s 

        """Overlap size of 0.75"""
        overlap_window = int(window_size * (1 - self.overlap))
        #print(overlap_window)
        increment_overlap = overlap_window
        self.prediction.put(0)

        time.sleep(4)
        while True:
            start = time.time()
 
            self.cortex.get_data(window=overlap_window)
            eeg_data = list(self.cortex.Q.queue)[increment_overlap:]
            print(len(eeg_data))
            self.di.append(self.model.run(eeg_data))

            if len(self.di) == 3:  # Every 3 prediction we change the direction of cube
                self.prediction.put(max(self.di,key=self.di.count)) # Maximum occured prediction
                #print(self.prediction.queue)
                self.di = []
                #self.di.append(self.prediction)  # To avoid empty list

            increment_overlap += overlap_window

            end = time.time() - start
            print(f'Live_prediction: {end}')
            


    def start_Live(self, bool):
        
        self.tr = Thread(target=self.live_prediction)
        self.tr.start()  
        #time.sleep(4)
        # Labels are: 'Rotate', 'Forward', 'Neutral', 'Stop'
        self.LT = LiveThread()
        self.LT.start()
        seq = ['Neutral', 'Forward','Rotate', 'Stop']
        while self.LT.running:
            start = time.time()
            print(self.prediction.get())
            direction = seq[int(self.prediction.get())]

            neutral_marker = {"Label": "Neutral", "Value": 0}
            forward_marker = {"Label": "Forward", "Value": 1}
            rotate_marker = {"Label": "Rotate", "Value": 2}
            stop_marker = {"Label": "Stop", "Value": 3}

            #order = [neutral_marker, forward_marker, rotate_marker, stop_marker]
            #shuffle(order)
            #print(order[0]['Value'])

            #print(direction)
            Cube = start_3Danimation(0.005, live_mode=True)
            #Cube.run_live(True, seq[order[0]['Value']])
            Cube.run_live(True, direction)
            end = time.time() - start
            print(f"Cube : {end}")
        try:
            quit_3Danimation()
        except:
            pass

    def keyPressEvent(self, QKeyEvent):
        # thread aufr??umen
        if QKeyEvent.key() == QtCore.Qt.Key_Q:
            self.LT.running = False
            self._stopThread()
            self.tr.join()

            print('pressed')

        elif QKeyEvent.key() == QtCore.Qt.Key_C:
            self.cortex.close_session()
            #info = self.cortex.terminateLink(streams=['dev'])

    def _stopThread(self):
        self.LT.close()
        self.LT.quit()
        self.LT.wait()

class LiveThread(QtCore.QThread):
    def __init__(self):
        super(LiveThread, self).__init__()
        self.running = True

    #update = QtCore.pyqtSignal(bool)
    def run(self):
        for i in range(300):
            time.sleep(1)
        self.running = False

def marker(value):

    mark = {
        "label": str(value),
        "value": value,
        "port": "python-app",
        "time": time.time()*1000
    }
    return mark

######################file management
import pathlib
class manage_file:
    '''
    Creates file directory of each user in the current folder
    this is where EEG file, marker file, joblib are stored

    '''
    def __init__(self):
        self.CURR_dir = pathlib.Path.cwd()  # you can change the default location of where the directories should be

    def make_dir(self, dir_name):
        self.folder = self.CURR_dir / dir_name
        try:
            self.path = self.folder.mkdir(parents=True, exist_ok=False)

        except FileExistsError:
            print('Exists')

        else:
            print('Created')
        folder = self.folder.__str__()
        return folder
