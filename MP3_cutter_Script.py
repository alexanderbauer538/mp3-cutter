# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 20:42:27 2019

@author: Alexander
"""


import pathlib
#from os import path
#from glob import glob 

import pydub



import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QAction, QMessageBox, QLabel
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QErrorMessage
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit


def function_cut_audio_file(audio_file_to_cut,start_time,stop_time):
    extract = audio_file_to_cut[start_time:stop_time]
    return extract





class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'Python mp3 file processor'
        self.left = 50
        self.top = 50
        self.width = 1200
        self.height = 800
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox_source_directory = QLineEdit(self)
        self.textbox_source_directory.move(200, 30)
        self.textbox_source_directory.resize(380,20)


        # create textboxes to input start and stop times for latter processing
        self.textbox_start_minutes = QLineEdit(self)
        self.textbox_start_minutes.move(20, 80)
        self.textbox_start_minutes.resize(80,20)
        self.textbox_start_minutes.setText('0')
        label = QLabel('Start minutes', self)
        label.move(20,80-25)
        self.textbox_start_seconds = QLineEdit(self)
        self.textbox_start_seconds.move(20, 120)
        self.textbox_start_seconds.resize(80,20)
        self.textbox_start_seconds.setText('0')
        label = QLabel('Start seconds', self)
        label.move(20,120-25)
        self.textbox_stop_minutes = QLineEdit(self)
        self.textbox_stop_minutes.move(20, 160)
        self.textbox_stop_minutes.resize(80,20)
        self.textbox_stop_minutes.setText('0')
        label = QLabel('Stop minutes', self)
        label.move(20,160-25)
        self.textbox_stop_seconds = QLineEdit(self)
        self.textbox_stop_seconds.move(20, 200)
        self.textbox_stop_seconds.resize(80,20)
        self.textbox_stop_seconds.setText('0')
        label = QLabel('Stop seconds', self)
        label.move(20,200-25)
        
        # Create textbox
        self.textbox_song_length = QLineEdit(self)
        self.textbox_song_length.move(20, 240)
        self.textbox_song_length.resize(50,20)
        label = QLabel('Total length', self)
        label.move(20,240-25)

        
        # Create textbox
        self.textbox_file_name = QLineEdit(self)
        self.textbox_file_name.move(200, 80)
        self.textbox_file_name.resize(300,20)
        label = QLabel('Filename', self)
        label.move(200,80-25)

        
        # Create textbox
        self.textbox_file_path = QLineEdit(self)
        self.textbox_file_path.move(200, 120)
        self.textbox_file_path.resize(300,20)
        label = QLabel('File Path', self)
        label.move(200,120-25)

        
        # Create a button in the window and connect it to the function
        # selecting the file
        self.select_button = QPushButton('Select File', self)
        self.select_button.move(20,340)        
        self.select_button.clicked.connect(self.select_File)

 
        
        # Create a button to process the file
        self.cut_button = QPushButton('Process File', self)
        self.cut_button.move(20,380)
        self.cut_button.clicked.connect(self.process_File)
                        
        # Create a button to close the GUI
        self.close_button = QPushButton('Close', self)
        self.close_button.move(20,420)
        
        # connect button to function on_click
        self.close_button.clicked.connect(self.close_GUI)
        
        
        self.show()
        
        

    @pyqtSlot()
    def close_GUI(self):
        ex.close()
        ex.destroy()
    

        
    
    @pyqtSlot()
    def process_File(self):
        start_minutes = int(self.textbox_start_minutes.text())
        start_seconds = int(self.textbox_start_seconds.text())
        start_time = start_minutes*60*1000+start_seconds*1000

        stop_minutes = int(self.textbox_stop_minutes.text())
        stop_seconds = int(self.textbox_stop_seconds.text())
        stop_time = stop_minutes*60*1000+stop_seconds*1000

        name_file_to_be_processed = 'new_' + self.textbox_file_name.text() + '.mp3'
        audio_file_to_cut = pydub.AudioSegment.from_mp3(self.textbox_file_path.text())
        if (stop_time > len(audio_file_to_cut)):
            QMessageBox.question(self, 'Errormessage','Song shorter than maximum time.', QMessageBox.Ok, QMessageBox.Ok)
            return
        processed_file = function_cut_audio_file(audio_file_to_cut,start_time,stop_time)
        processed_file.export(name_file_to_be_processed, format="mp3")
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + str(start_time), QMessageBox.Ok, QMessageBox.Ok)
        #self.textbox_start_minutes.setText("")
        #self.close()
        
    @pyqtSlot()
    # function to open file selection dialogue which gets the name of the file
    # and its path and saves them in separate textboxes  
    def select_File(self):   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            selected_file_path = pathlib.Path(fileName)
            self.textbox_file_path.setText(fileName)
            self.textbox_file_name.setText(pathlib.Path(selected_file_path).stem)
            audio_file_to_cut = pydub.AudioSegment.from_mp3(self.textbox_file_path.text())
            song_length = len(audio_file_to_cut)/1000
            self.textbox_song_length.setText(str(int(song_length//60))+':'+str(int(song_length%60)))
            

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())




