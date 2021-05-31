from PyQt5.QtWidgets import QApplication, QGridLayout, QListWidgetItem ,QWidget, QHBoxLayout ,QFileDialog, QComboBox, QPushButton, QLineEdit, QLabel, QScrollArea
from PyQt5 import QtCore, QtGui, QtWidgets
from TestPage import TestPage

class ContactQuality(QWidget):
    def __init__(self, name, parent, pos):
        super().__init__()

        # Section for general settings
        self.setGeometry(300, 300, 1213, 800)
        self.move(pos)
        self.setFixedHeight(800)
        self.setFixedWidth(1213)
        self.setWindowTitle("BCI - Machine Control through EEG - Contact Quality")

        self.parent = parent
        self.name = name

        self.background = QLabel(self)
        self.background.setGeometry(-690, -30, 2341, 831)
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("Visuals/background1.png"))
        self.background.setObjectName("background")

        # Section for setting labels with text for better understanding and overview
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(280, 170, 1081, 311)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Please calibrate Headset until the Contact Quality is green to assure \n" 
                                "best results.")
        self.label_2.setStyleSheet("color: rgb(2, 150, 211)")


        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(280, 370, 1051, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("1.  Move the whole headset to adjust reference marker \n"
                                                "    and get a first overall contact.")
        self.label_3.setStyleSheet("color: rgb(2, 150, 211)")

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(280, 410, 731, 41)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("2.  Work with each electrode to adjust contact quality until it is green.")
        self.label_4.setStyleSheet("color: rgb(2, 150, 211)")

        self.label_5 = QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(280, 500, 751, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Tip Section for better signal strength.")
        self.label_5.setStyleSheet("color: rgb(2, 150, 211)")

        self.label_6 = QLabel(self)
        self.label_6.setGeometry(280, 540, 751, 41)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("- Remove hair between scalp and electrode")
        self.label_6.setStyleSheet("color: rgb(2, 150, 211)")


        self.label_7 = QLabel(self)
        self.label_7.setGeometry(280, 570, 751, 41)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("- Move close to the USB-Dongle for best signal strength")
        self.label_7.setStyleSheet("color: rgb(2, 150, 211)")

        self.label_8 = QLabel(self)
        self.label_8.setGeometry(280, 610, 761, 41)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_8.setText("- Close all unnecessary Bluetooth Connections and disable the \n"
                                                "   Bluetooth function on devices in the room ")
        self.label_8.setStyleSheet("color: rgb(2, 150, 211)")

        self.label_9 = QLabel(self)
        self.label_9.setGeometry(280, 220, 461, 61)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_9.setText("EPOC+ Calibration")
        self.label_9.setStyleSheet("color: rgb(2, 150, 211)")

        # Section for adding buttons to navigate
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(1040, 730, 113, 32)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Training Page")

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(40, 730, 113, 32)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Back")

        # Adding functionality to buttons
        self.pushButton.clicked.connect(lambda: self.move_to_TestPage(self.name, self))
        self.pushButton_2.clicked.connect(self.move_back)


    def move_to_TestPage(self, name, parent):
        pos = self.pos()
        self.TP = TestPage(name, parent, pos)
        self.TP.show()
        self.hide()

    def move_back(self):
        pos = self.pos()
        self.parent.move(pos)
        self.parent.show()
        self.close()


# This part is not visualized in the current versionb but can be used if needed
# Small adjustments need to be done, because the cortex file changed and the following art was not updated

# Also test functions are there so you can see how it should work in the normal case

class PlotGraph(FigureCanvasQTAgg, anim.FuncAnimation):
    def __init__(self, parent, cortex):

        self.cortex = cortex

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        cmap, norm = self.create_colormap()
        self.img, self.frame, self.color_dict = self.contact_quality_plot_initialize()

        self.scat = self.ax.scatter(self.frame['x_Axis'], self.frame['y_Axis'], linewidths=1, s=750, c=self.frame['CQ'], cmap=cmap, norm=norm, edgecolors="#000000")
        self.scat.axes.get_xaxis().set_visible(False)
        self.scat.axes.get_yaxis().set_visible(False)
        self.ax.imshow(self.img, extent=[0, 1480, 0, 1496])
        self.fig.subplots_adjust(bottom=0.05, top=0.95, right=1.15, left=0.1)
        self.fig.set_facecolor('#0296D3')

        print('test1')
        #self.timer = self.startTimer(1000)
        anim.FuncAnimation.__init__(self, self.fig, self.ani, fargs=(cmap, self.scat), interval=100)

    def create_colormap(self):
        cmap = colors.ListedColormap(['slategrey', 'red', 'orange', 'gold', 'springgreen'])
        bounds = [0.0, 1.0, 2.0, 3.0, 4.0]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        return cmap, norm

    def ani(self, evt, i, scat):
        frame = self.get_API_Update(self.frame)
        update = frame['CQ']

        if frame['CQ'][14] == 4.0:
            self.fig.set_facecolor('springgreen')
        else:
            self.fig.set_facecolor('#0296D3')

        scat.set_array(np.array(update))
        return scat

    def timereEvent(self, evt):
        self.frame = self.test_plot(self.frame)
        print(self.frame)
        frame = self.test_plot(self.frame)
        for index, row in frame.iterrows():
            scat = self.ax.scatter(row['x_Axis'], row['y_Axis'], linewidths=1, s=750, facecolors=self.color_dict[row['CQ']],
                               edgecolors="#000000")
            col = self.color_dict[row['CQ']]
        scat.axes.get_xaxis().set_visible(False)
        scat.axes.get_yaxis().set_visible(False)
        self.ax.imshow(self.img, extent=[0, 1480, 0, 1496])
        self.fig.subplots_adjust(bottom=0.05, top=0.95, right=1.15, left=0.1)
        self.fig.set_facecolor(col)

        self.fig.canvas.draw()

    def get_API_Update(self, dataframe):
        try:
            if self.cortex.Q_DEV.empty() != True:
                val = self.cortex.Q_DEV.get()
                api_CQ_update = val[2]
                for index, row in dataframe.iterrows():
                    dataframe.at[index, 'CQ'] = api_CQ_update[index]

        except:
            print('no update')

        finally:
            return dataframe

    def test_plot(self, dataframe):
        list = [0.0, 1.0, 2.0, 3.0, 4.0]
        for index, row in dataframe.iterrows():
            random.shuffle(list)
            dataframe.at[index, 'CQ'] = list[2]
        print(dataframe['CQ'])

        return dataframe

    def contact_quality_plot_initialize(self):
        self.contact_quality_frame = pd.DataFrame(columns=['Electrode', 'x_Axis', 'y_Axis', 'CQ'])


        self.contact_quality_frame['Electrode'] = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6',
                                              'F4', 'F8', 'AF4', 'Overall']

        self.contact_quality_frame['x_Axis'] = np.array(
            [570, 390, 570, 400, 280, 435, 570, 855, 1000, 1150, 1030, 1035, 855, 855, -50])

        self.contact_quality_frame['y_Axis'] = np.array(
            [1065, 1000, 820, 810, 695, 345, 160, 160, 345, 695, 810, 1000, 820, 1065, -50])

        self.contact_quality_frame['CQ'] = 0.0

        color_dict = {0.0: '#A9A9A9', 1.0: '#FF3333', 2.0: '#FF7F50', 3.0: '#FFD700', 4.0: '#00FF09'}

        img = plt.imread('electrodes.png')

        print(self.contact_quality_frame)

        return img, self.contact_quality_frame, color_dict


