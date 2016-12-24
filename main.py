import sys
import cv2
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from dialog import Ui_dialog
import ImageProcessingLibrary

MAX_HUE = 179
MAX_SAT = 255
MAX_VAL = 255

TIMER_INTERVAL = 500

class MyForm(QtGui.QDialog):
    HSVColorFilter = ImageProcessingLibrary.HSVColorFilter()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_dialog()
        self.ui.setupUi(self)

        ###########################################################
        # Connect Signal
        ###########################################################
        self.ui.horizontalSlider_lowHue.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_lowSat.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_lowVal.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_highHue.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_highSat.valueChanged.connect(self.updateSlider)
        self.ui.horizontalSlider_highVal.valueChanged.connect(self.updateSlider)

        self.ui.spinBox_lowHue.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_lowSat.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_lowVal.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_highHue.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_highSat.valueChanged.connect(self.updateSpinboxValue)
        self.ui.spinBox_highVal.valueChanged.connect(self.updateSpinboxValue)

        self.ui.pushButton_loadImage.clicked.connect(self.openImageFile)
        

        ###########################################################
        # Initial value 
        ###########################################################
        # Init slider value for high Threshold
        self.ui.horizontalSlider_highHue.setValue(MAX_HUE)
        self.ui.horizontalSlider_highSat.setValue(MAX_SAT)
        self.ui.horizontalSlider_highVal.setValue(MAX_VAL)
        # Init line edi
        self.ui.spinBox_highHue.setValue(MAX_HUE)
        self.ui.spinBox_highSat.setValue(MAX_SAT)
        self.ui.spinBox_highVal.setValue(MAX_VAL)
        # Set scaled properties
        self.ui.label_initialImage.setScaledContents(True)
        self.ui.label_finalImage.setScaledContents(True)

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateResultImage)
        self.timer.start(TIMER_INTERVAL)

        self.isImageValid = False

    def updateResultImage(self):
        low_Hue = self.ui.horizontalSlider_lowHue.value()
        low_Sat = self.ui.horizontalSlider_lowSat.value()
        low_Val = self.ui.horizontalSlider_lowVal.value()
        high_Hue = self.ui.horizontalSlider_highHue.value()
        high_Sat = self.ui.horizontalSlider_highSat.value()
        high_Val = self.ui.horizontalSlider_highVal.value()
        
        # Please note that we send value in RGB format
        # But openCV process in GRB. Additional processing is handled in ImageProcessingLibrary blass
        self.HSVColorFilter.filterImage((low_Hue, low_Sat, low_Val), (high_Hue, high_Sat, high_Val))
        self.showFilteredImage()

    def openImageFile(self):
        fileDlg = QFileDialog.getOpenFileName(self, "Open Image", "", "Any file (*.*);;Image file(*.jpg *.gif *.png)")
        if self.HSVColorFilter.loadImage(str(fileDlg)) == False:
            # Add messagebox error message here
            print "Cannot Load Image"
            self.isImageValid = False
        else:
            self.isImageValid = True
            self.showOriginalImage()

    def showAllImage(self):
        if self.isImageValid:
            self.showOriginalImage()
            self.showFilteredImage()

    def showOriginalImage(self):
        if self.isImageValid == True:
            # Convert BGR to RGB
            self.cvOriginalImage = self.HSVColorFilter.getOriginalImage()
            # print self.cvOriginalImage
            self.cvOriginalImage = cv2.cvtColor(self.cvOriginalImage, cv2.COLOR_HSV2RGB)
            # Get image properties
            height, width, byteValue = self.cvOriginalImage.shape

            # Convert to QPixmap
            self.qImageData = QImage(self.cvOriginalImage, width, height, QtGui.QImage.Format_RGB888)
            self.qPixmapData = QtGui.QPixmap.fromImage(self.qImageData)

            # scale and place on label
            self.ui.label_initialImage.setPixmap(self.qPixmapData)

    def showFilteredImage(self):
        if self.isImageValid:
            # Convert BGR to RGB
            self.cvFinalImage = self.HSVColorFilter.getFilteredImage()
            # print self.cvOriginalImage
            self.cvFinalImage = cv2.cvtColor(self.cvFinalImage, cv2.COLOR_HSV2RGB)
            # Get image properties
            height, width, byteValue = self.cvFinalImage.shape

            # Convert to QPixmap
            self.qImageData = QImage(self.cvFinalImage, width, height, QtGui.QImage.Format_RGB888)
            self.qPixmapData = QtGui.QPixmap.fromImage(self.qImageData)

            # scale and place on label
            self.ui.label_finalImage.setPixmap(self.qPixmapData)

    def updateSlider(self):
        # self.ui.lineEdit_lowRed.setValue(str(self.ui.horizontalSlider_lowHue.value()))
        self.ui.spinBox_lowHue.setValue(self.ui.horizontalSlider_lowHue.value())
        self.ui.spinBox_lowSat.setValue(self.ui.horizontalSlider_lowSat.value()) 
        self.ui.spinBox_lowVal.setValue(self.ui.horizontalSlider_lowVal.value())
        self.ui.spinBox_highHue.setValue(self.ui.horizontalSlider_highHue.value())
        self.ui.spinBox_highSat.setValue(self.ui.horizontalSlider_highSat.value())
        self.ui.spinBox_highVal.setValue(self.ui.horizontalSlider_highVal.value())  
         
    def updateSpinboxValue(self):
        self.ui.horizontalSlider_lowHue.setValue(self.ui.spinBox_lowHue.value())
        self.ui.horizontalSlider_lowSat.setValue(self.ui.spinBox_lowSat.value())
        self.ui.horizontalSlider_lowVal.setValue(self.ui.spinBox_lowVal.value())
        self.ui.horizontalSlider_highHue.setValue(self.ui.spinBox_highHue.value())
        self.ui.horizontalSlider_highSat.setValue(self.ui.spinBox_highSat.value())
        self.ui.horizontalSlider_highVal.setValue(self.ui.spinBox_highVal.value())

    def closeApp(self):
        sys.exit(9)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())