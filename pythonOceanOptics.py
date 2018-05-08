#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 13:35:56 2017

@author: rsfontenot
"""

from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from QLed import QLed
from Light import Spectrometer as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyqtgraph as pg

import sys
import os
import random
import time
import numpy as np
import pylab
import h5py
import scipy

global spec
wavelength = [] #[i for i in range(1000)]
intensity = [] #[random.random() for i in range(1000)]

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Spectrometer Software'
        self.left = 100
        self.top = 100
        self.width = 1500
        self.height = 800
        self.initUI()
        
        
        
    def initUI(self):
        
        self.setStyleSheet("QPushButton {background-color: rgb(227,119,100); font: bold}")
        
        # Creating LEDs
        #Initialize Spectrometer LED
        self.SpectrometerIndicator = QLed(onColour=QLed.Green, offColour = QLed.Red, shape=QLed.Circle)
        self.SpectrometerIndicator.value = False
        # Get Data LED
        self.SingleModeIndicator = QLed(onColour=QLed.Green, offColour = QLed.Red, shape=QLed.Circle)
        self.SingleModeIndicator.value = False
        #Continuous Mode
        self.ContinuousModeIndicator = QLed(onColour=QLed.Green, offColour = QLed.Red, shape=QLed.Circle)
        self.ContinuousModeIndicator.value = False
        
        self.integrationTime = QSpinBox()
        self.integrationTime.setMinimum(1000) # 1 ms minimum
        self.integrationTime.setMaximum(10000000) # 10 s maximum
        self.integrationTime.setValue(1000000) # 1 s is default
        
        
        # Creating Buttons
        exitBtn = QPushButton('Quit')
        #exitBtn.addStretch()
        exitBtn.clicked.connect(self.close_application)
        exitBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.initSpectrometer = QPushButton('Initialize Spectrometer')
        self.initSpectrometer.setFixedWidth(150)
        self.initSpectrometer.setCheckable(True)
        #self.initSpectrometer.setStyleSheet("QPushButton {background-color: rgb(227,119,100)}")
        self.initSpectrometer.clicked.connect(self.initializeSpectrometer)
        
        self.SingleMode = QPushButton('Single Mode')
        self.SingleMode.setFixedWidth(150)
        self.ContinuousMode = QPushButton('Continuous Mode')
        self.ContinuousMode.setFixedWidth(150)
        
        
        self.setIntegrationTimeButton = QPushButton('Set Integration Time (µs)')
        self.setIntegrationTimeButton.setFixedWidth(150)
        self.setIntegrationTimeButton.clicked.connect(self.setSpecIntTime)
        
        self.directoryPath = os.getcwd()
        self.directory = QLineEdit('Save Location: '+ self.directoryPath)
        self.directory.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        

        
        # Main Layout
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        
        
        #Top layout
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.directory,10)
        topLayout.addWidget(exitBtn,1)
        
        # Middle Layout
        middleLayout = QHBoxLayout()
        

        
        
        #middleLayout.addStretch(1)

        options = QPushButton('Options')
        options.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        #Plotting section

               
        #self.graphPlot = PlotCanvas(self, width = 5, height = 4)
        #graphPlot.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        self.graphPlot = pg.PlotWidget(name = 'Luminescence Spectrum')
        self.luminescencePlot = self.graphPlot.plot(wavelength, intensity)
        self.luminescencePlot.setPen((0,0,0))
        
        
        
        #Options Layout
        
        optionsLayout = QVBoxLayout()
        optionsLayout.setAlignment(Qt.AlignTop)
        
        
        labelLayout = QHBoxLayout()
        specLabel = QLabel('Spectrometer \n')
        specLabel.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 16px; color: navy}")
        labelLayout.addWidget(specLabel)
        labelLayout.addWidget(QLabel())
        
        
        step1Layout = QHBoxLayout()
        step1 = QLabel('Step 1: Initialize Spectrometer \n')
        step1.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step1Layout.addWidget(step1)
        step1Layout.addWidget(QLabel())
        
        
        initLayout = QHBoxLayout()
        initLayout.addWidget(self.SpectrometerIndicator)
        initLayout.addWidget(self.initSpectrometer)
        initLayout.setAlignment(Qt.AlignLeft)
        
        step2Layout = QHBoxLayout()
        step2 = QLabel('\n Step 2: Set the Integration Time \n')
        step2.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step2Layout.addWidget(step2)
        step2Layout.addWidget(QLabel())
        
        step3Layout = QHBoxLayout()
        step3 = QLabel('\n Step 3: Set the Acquisition Mode \n')
        step3.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step3Layout.addWidget(step3)
        step3Layout.addWidget(QLabel())
        
        step4Layout = QHBoxLayout()
        step4 = QLabel('\n Step 4: Change Save Directory (Optional) \n')
        step4.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step4Layout.addWidget(step4)
        step4Layout.addWidget(QLabel())
        
        step5Layout = QHBoxLayout()
        step5 = QLabel('\n Step 5: Begin Taking Spectra \n')
        step5.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step5Layout.addWidget(step5)
        step5Layout.addWidget(QLabel())
        
        step6Layout = QHBoxLayout()
        step6 = QLabel('\n Step 6: Set Background (Optional) \n')
        step6.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step6Layout.addWidget(step6)
        step6Layout.addWidget(QLabel())

        step7Layout = QHBoxLayout()
        step7 = QLabel('\n Step 7: Subtract Background (Optional) \n')
        step7.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step7Layout.addWidget(step7)
        step7Layout.addWidget(QLabel())      
        
        step8Layout = QHBoxLayout()
        step8 = QLabel('\n Step 8: Begin Saving \n')
        step8.setStyleSheet("QLabel {font: bold Large; font-family: 'Times New Roman'; font-size: 14px; color: black}")
        step8Layout.addWidget(step8)
        step8Layout.addWidget(QLabel())
        
        
        
        singleModeLayout = QHBoxLayout()
        singleModeLayout.addWidget(self.SingleModeIndicator)
        singleModeLayout.addWidget(self.SingleMode)
        singleModeLayout.setAlignment(Qt.AlignLeft)
        
        continuousModeLayout = QHBoxLayout()
        continuousModeLayout.addWidget(self.ContinuousModeIndicator)
        continuousModeLayout.addWidget(self.ContinuousMode)
        continuousModeLayout.setAlignment(Qt.AlignLeft)
        
        acqLayout = QVBoxLayout()
        acqLayout.setAlignment(Qt.AlignLeft)
        self.specSetting = QButtonGroup()
        self.singleAcq = QRadioButton('Single Acquisition')
        self.specSetting.addButton(self.singleAcq)
        self.continuousAcq = QRadioButton('Continuous Acquisition')
        self.continuousAcq.setChecked(True)
        self.specSetting.addButton(self.continuousAcq)
        acqLayout.addWidget(self.singleAcq)
        acqLayout.addWidget(self.continuousAcq)
        
        #Integration Time
        integrationTimeLayout = QHBoxLayout()
        integrationTimeLayout.addWidget(self.integrationTime)
        integrationTimeLayout.addWidget(self.setIntegrationTimeButton)
        
        #Set Directory
        setDirectoryLayout = QVBoxLayout()
        setDirectoryLayout.setAlignment(Qt.AlignCenter)
        self.setDirectory = QPushButton('Set Directory')
        self.setDirectory.setFixedWidth(150)
        self.setDirectory.setCheckable(True)
        self.changeDirectory = QPushButton('Change Save Location')
        self.changeDirectory.setFixedWidth(150)
        self.changeDirectory.clicked.connect(self.newDirectory)
        self.changeDirectory.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
        self.changeDirectory.setCheckable(False)
        setDirectoryLayout.addWidget(self.changeDirectory)
        #setDirectoryLayout.setSpacing(10)
        #setDirectoryLayout.addWidget(self.setDirectory)
        
        #Run and Stop Spectra
        self.startRun = QPushButton('Start')
        self.startRun.setFixedWidth(150)
        self.startRun.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
        self.startRun.setCheckable(False)
        self.startRun.clicked.connect(self.plotSpectra)
        self.stopRun = QPushButton('Stop')
        self.stopRun.setFixedWidth(150)
        self.stopRun.setCheckable(True)
        self.stopRun.setStyleSheet("QPushButton {background-color: rgb(237,244,19)}")
        RunningLayout = QHBoxLayout()
        RunningLayout.setAlignment(Qt.AlignCenter)
        RunningLayout.addWidget(self.startRun)
        RunningLayout.addSpacing(8)
        RunningLayout.addWidget(self.stopRun)
        
        #Add Set Background Button

        self.setBackground = QPushButton('Set Background')
        self.setBackground.setFixedWidth(150)
        self.setBackground.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
        self.setBackground.setCheckable(True)
        setBackgroundLayout = QHBoxLayout()
        setBackgroundLayout.setAlignment(Qt.AlignCenter)
        setBackgroundLayout.addWidget(self.setBackground)
        
        
        # Subtract background layout
        self.subtractBackground = QPushButton('Subtract Background')
        self.subtractBackground.setFixedWidth(150)
        self.subtractBackground.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
        self.subtractBackground.setCheckable(True)
        self.undoBackground = QPushButton('Undo Background')
        self.undoBackground.setFixedWidth(150)
        self.undoBackground.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
        self.undoBackground.setCheckable(True)
        backgroundLayout = QHBoxLayout()
        backgroundLayout.addWidget(self.subtractBackground)
        backgroundLayout.addSpacing(8)
        backgroundLayout.addWidget(self.undoBackground)
        
        
        
        #Add save button
        
        self.saveSpectraMat = QPushButton('Save as .mat')
        self.saveSpectraMat.setFixedWidth(150)
        self.saveSpectraMat.setCheckable(True)
        #self.saveSpectraTxt.setFixedHeight(60)
        #self.saveSpectraTxt.setStyleSheet("QPushButton {background-color: rgb(0,191,255)}")
        self.saveSpectraMat.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
        self.saveSpectraBin = QPushButton('Save as .hdf5')
        self.saveSpectraBin.setFixedWidth(150)
        self.saveSpectraBin.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
        self.saveSpectraBin.setCheckable(True)
        #self.saveSpectraBin.clicked.connect(self.saveBinPressed)
        saveSpectralayout = QHBoxLayout()
        saveSpectralayout.setAlignment(Qt.AlignCenter)
        saveSpectralayout.addWidget(self.saveSpectraMat)
        saveSpectralayout.addSpacing(8)
        saveSpectralayout.addWidget(self.saveSpectraBin)
        
        
        
        
        optionsLayout.addLayout(labelLayout)
        optionsLayout.addLayout(step1Layout)
        optionsLayout.addLayout(initLayout)
        optionsLayout.addLayout(step2Layout)
        optionsLayout.addLayout(integrationTimeLayout)
        optionsLayout.addLayout(step3Layout)
        optionsLayout.addLayout(acqLayout)
        optionsLayout.addLayout(step4Layout)
        optionsLayout.addLayout(setDirectoryLayout)
        optionsLayout.addLayout(step5Layout)
        optionsLayout.addLayout(RunningLayout)
        optionsLayout.addLayout(step6Layout)
        optionsLayout.addLayout(setBackgroundLayout)
        optionsLayout.addLayout(step7Layout)
        optionsLayout.addLayout(backgroundLayout)
        optionsLayout.addLayout(step8Layout)
        optionsLayout.addLayout(saveSpectralayout)
        #optionsLayout.addLayout()
        
        
        
        #optionsLayout.addLayout(singleModeLayout)
        #optionsLayout.addLayout(continuousModeLayout)
        
        
        
        
        #Putting middle layout together
        
        #middleLayout.addLayout(labelLayout)
        middleLayout.addLayout(optionsLayout)
        #middleLayout.addWidget(options,2)
        middleLayout.addWidget(self.graphPlot,9)
        
        #Bottom Layout
        bottomLayout = QHBoxLayout()
        self.outputMessages = QLineEdit()
        self.outputMessages.setObjectName("outputMessages")
        self.outputMessages.setText("Output Messages")
        self.outputMessages.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.progressBar = QProgressBar()
        self.progressBar.resize(120,100)
        self.progressBar.setValue(0)
        #progressBar.setMinimumWidth(200)
        #progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        bottomLayout.addWidget(self.outputMessages,8)
        bottomLayout.addWidget(self.progressBar)
        
       
        
        
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(middleLayout)
        mainLayout.addLayout(bottomLayout)
        
        self.setLayout(mainLayout)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.move(50,20)
        self.show()

        


    def close_application(self):
        self.outputMessages.setText("Program is closing")
        time.sleep(2) #This pauses the program for 3 seconds
        sys.exit()
        
        
    def initializeSpectrometer(self):
                       
        if self.SpectrometerIndicator.value == False:
            self.outputMessages.setText("Spectrometer is initializing")
            self.spec = sb.initalizeOceanOptics() #Establishes communication with the spectrometer
            for x in range(1,5):
                time.sleep(0.5)
                self.progressBar.setValue(x/4*100)
            self.SpectrometerIndicator.value = True
            self.outputMessages.setText("Spectrometer is ready to go")
            self.initSpectrometer.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
            return self.spec
        else:
            self.outputMessages.setText("Spectrometer is disconnecting")
            sb.closeSpectrometer(self.spec)
            for x in range(1,5):
                time.sleep(0.5)
                self.progressBar.setValue(x/4*100)
            self.SpectrometerIndicator.value = False #Closes the spectrometer
            self.outputMessages.setText("Spectrometer has been disconnected")
            self.initSpectrometer.setStyleSheet("QPushButton {background-color: rgb(227,119,100)}")
            
    def setSpecIntTime(self):
        time = self.integrationTime.value()
        #for x in range(1,4):
            #time.sleep(0.5)
            #self.progressBar.setValue(x/3*100)
        sb.setIntegrationTime(time)
        self.outputMessages.setText("Integration time has been set to "+ str(time/1000) + " ms")
        self.setIntegrationTimeButton.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
       
        
    def newDirectory(self):
        self.directoryPath = QFileDialog.getExistingDirectory(self,"Choose a Directory to Save the data")
        self.directory.setText('Save Location: '+ self.directoryPath)
        return self.directoryPath

    
    def plotSpectra(self):
        t = self.integrationTime.value()
        x=1
        checked = False
        if self.singleAcq.isChecked():
            print("Im in single mode")
            wavelength = sb.getWavelength()
            intensity = sb.getIntensity()
            pg.QtGui.QApplication.processEvents()
            print("Interation : " + str(x))
            self.outputMessages.setText("Spectrum " + str(x))
            self.luminescencePlot = self.graphPlot.plot(wavelength, intensity, clear = True, pen = pg.mkPen('r'))
            font = QFont('Times New Roman', 12)
            labelStyle = {'color': 'k', 'font-size': '10pt'}
            self.graphPlot.setLabel('bottom', text = 'Wavelength (nm)', **labelStyle)
            self.graphPlot.setLabel('left', text = 'Intensity (a.u.)',**labelStyle)
            time.sleep(t/1000000)
        else:
            while self.stopRun.isChecked() == False:
                if self.setBackground.isChecked():
                    print('Background set button is pressed')
                    wavelength = sb.getWavelength()
                    backgroundIntensity = sb.getIntensity()
                    intensity = backgroundIntensity 
                    x = x+1
                    pg.QtGui.QApplication.processEvents()
                    self.outputMessages.setText("Background spectrum has been set")
                    self.setBackground.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    time.sleep(t/1000000)
                    self.setBackground.setChecked(False)
                    
                    
                if self.subtractBackground.isChecked():
                    checked = True
                    self.subtractBackground.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    self.subtractBackground.setChecked(False)
                    if self.saveSpectraBin.isChecked():
                        name = os.path.join(self.directoryPath,'BackgroundSpectrum.h5')
                        f = h5py.File(name, "w")
                        f.create_dataset('Background Subtracted', data=True)
                        f.create_dataset('Wavelength', data=wavelength)
                        f.create_dataset('Intensity', data=intensity)
                        f.close()
                        self.saveSpectraBin.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    else:
                        self.saveSpectraBin.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
                    
                    if self.saveSpectraMat.isChecked():
                        name = os.path.join(self.directoryPath,'BackgroundSpectrum')
                        data = {'Background Subtraction': True,
                                'Wavelength': wavelength,
                                'Intensity': intensity}
                        scipy.io.savemat(name, mdict=data, appendmat = True)
                        self.saveSpectraMat.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    else:
                        self.saveSpectraMat.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
                        
                
                if self.undoBackground.isChecked() == True:
                    checked = False
                    self.subtractBackground.setChecked(False)
                    self.subtractBackground.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
                    self.undoBackground.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
                    self.undoBackground.setChecked(False)
                
                if checked:
                    wavelength = sb.getWavelength()
                    rawIntensity = sb.getIntensity()
                    intensity = rawIntensity - backgroundIntensity
                    if self.saveSpectraBin.isChecked():
                        name = os.path.join(self.directoryPath, 'Spectrum'+str(x)+'_Background_subtracted.h5')
                        f = h5py.File(name, "w")
                        f.create_dataset(name, data=True)
                        f.create_dataset('Wavelength', data=wavelength)
                        f.create_dataset('Intensity', data=intensity)
                        f.close()
                        self.saveSpectraBin.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    else:
                        self.saveSpectraBin.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
                        
                    if self.saveSpectraMat.isChecked():
                        name = os.path.join(self.directoryPath,'Spectrum'+str(x)+'_Background_subtracted')
                        data = {'Background Subtraction': True,
                                'Wavelength': wavelength,
                                'Intensity': intensity}
                        scipy.io.savemat(name, mdict=data, appendmat = True)
                        self.saveSpectraMat.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    else:
                        self.saveSpectraMat.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
                else:
                    wavelength = sb.getWavelength()
                    intensity = sb.getIntensity()
                    if self.saveSpectraBin.isChecked():
                        name = os.path.join(self.directoryPath, 'Spectrum'+str(x)+'_No_Background.h5')
                        f = h5py.File(name, "w")
                        f.create_dataset(name, data=False)
                        f.create_dataset('Wavelength', data=wavelength)
                        f.create_dataset('Intensity', data=intensity)
                        f.close()
                        self.saveSpectraBin.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    else:
                        self.saveSpectraBin.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")
                        
                    if self.saveSpectraMat.isChecked():
                        name = os.path.join(self.directoryPath,'Spectrum'+str(x)+'_No_Background')
                        data = {'Background Subtraction': True,
                                'Wavelength': wavelength,
                                'Intensity': intensity}
                        scipy.io.savemat(name, mdict=data, appendmat = True)
                        self.saveSpectraMat.setStyleSheet("QPushButton {background-color: rgb(85,225,0)}")
                    else:
                        self.saveSpectraMat.setStyleSheet("QPushButton {background-color: rgb(255,255,255)}")                    
    
                pg.QtGui.QApplication.processEvents()
                #print("Interation : " + str(x))
                self.outputMessages.setText("Spectrum " + str(x))
                self.luminescencePlot = self.graphPlot.plot(wavelength, intensity, clear = True, pen = pg.mkPen('r'))
                font = QFont('Times New Roman', 12)
                labelStyle = {'color': 'k', 'font-size': '10pt'}
                self.graphPlot.setLabel('bottom', text = 'Wavelength (nm)', **labelStyle)
                self.graphPlot.setLabel('left', text = 'Intensity (a.u.)',**labelStyle)
                #self.graphPlot.getAxis('bottom').labelFont = font
                #self.graphPlot.getAxis('left').labelFont = font
                time.sleep(t/1000000)
                x = x+1
            #self.graphPlot.clear()
            
            #if self.stopRun.isChecked()== True:
                #self.outputMessages.setText("Data collection has ceased")
                #break
                


#This creates the actual window when Python runs and keeps it running until 
# you close the window
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())