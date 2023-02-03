# -*- coding: utf-8 -*-
"""

Benjamin Gansemer
Started: November 2017
Last updated: February 2023

Image Coder

This program uses a GUI to code images or other files. The interface allows users to 
provide a folder with images, a folder in which to save the coded images,
and an excel spreadsheet to serve as a database to keep track of images and 
their codes, allowing users to decode the images later. 
Images can be in any format. The image folder and 
save folder must be different from each other. The spreadsheet must be 
an excel spreadsheet. The updated spreadsheet will be saved as
'originalDB_updated'. 

New from version 1.0: can now traverse an entire directory. Images can be
in more than one folder, provided all folders are present in a root folder.
Minor updates to the GUI, including tip boxes and version specification in the
main window title.


"""

'''
TODO: allow for an empty template, or providing no excel file.
'''

from PyQt5.QtWidgets import (QMainWindow, QInputDialog,QFileDialog, QDesktopWidget,
                             QApplication, QPushButton, QLineEdit, QMessageBox,
                             QToolTip, qApp, QAction)
import sys
import os
from random import randint
import pandas
import shutil
from datetime import datetime as dt
#import openpyxl

class ImageCoder(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        #initialize UI
        self.initUI()
        
    def initUI(self):
        
        #Buttons
        self.imageDirBtn = QPushButton('Image File Path', self)
        self.imageDirBtn.move(20, 60)
        self.imageDirBtn.resize(125, 25)
        self.imageDirBtn.setToolTip('Click to select folder with original images')
        self.imageDirBtn.clicked.connect(self.getImageDir)
        
        self.imageSaveBtn = QPushButton('Image Save Path', self)
        self.imageSaveBtn.move(20, 100)
        self.imageSaveBtn.resize(125, 25)
        self.imageSaveBtn.setToolTip('Click to select a folder to save coded images in')
        self.imageSaveBtn.clicked.connect(self.getSaveDir)
        
        self.imageDbBtn = QPushButton('Spreadsheet File', self)
        self.imageDbBtn.move(20, 140)
        self.imageDbBtn.resize(125, 25)
        self.imageDbBtn.setToolTip('Click to select spreadsheet to store codes')
        self.imageDbBtn.clicked.connect(self.getImageDB)
        
#        self.imageDbPath = QPushButton('Spreadsheet Folder', self)
#        self.imageDbPath.move(20, 160)
        
        #button to start the coder
        self.coderBtn = QPushButton('Code Images', self)
        self.coderBtn.move(125, 220)
        self.coderBtn.setToolTip('Click to code images!')
        self.coderBtn.clicked.connect(self.codeImages)
        
        #LineEdits
        self.imageDirLe = QLineEdit(self)
        self.imageDirLe.move(160, 60)
        self.imageDirLe.resize(200, 25)
        
        self.imageSaveLe = QLineEdit(self)
        self.imageSaveLe.move(160, 100)
        self.imageSaveLe.resize(200, 25)
        
        self.imageDBLe = QLineEdit(self)
        self.imageDBLe.move(160, 140)
        self.imageDBLe.resize(200, 25)
        
#        self.imageDBPathLe = QLineEdit(self)
#        self.imageDBPathLe.move(140, 160)
#        self.imageDBPathLe.resize(200, 25)
        
        #other attributes
        self.imageDir = None
        self.saveDir = None
        self.newDB = None
        
#        exitAct = QAction('&Exit', self)
#        exitAct.setShortcut('Ctrl+Q')
#        exitAct.setStatusTip('Exit application')
#        exitAct.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        
        #placeholder menu in case other functionalities are added
        fileMenu = menubar.addMenu('&File')
#        fileMenu.addAction(exitAct)
        
        #set main window size and location
        self.setGeometry(300, 300, 380, 300)
        self.center()
        self.setWindowTitle('Image Coder v1.1')
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
  
    def getImageDir(self):
        '''
        Creates a FileDialog allowing user to choose the folder in which 
        the original images are located. Initiated by clicking the 
        'Image File Path' button. After selecting a folder, the path will be
        displayed next to the button.
        '''
        
        self.imageDir = QFileDialog.getExistingDirectory(self, 'Set Image Folder')
        self.imageDirLe.setText(self.imageDir)
       
        return self.imageDir
    
    def getSaveDir(self):
        '''
        Creates a FileDialog allowing user to choose the folder in which 
        the coded images will be saved. This must be different than the folder
        in which the original images are located. Initiated by clicking the
        'Image Save Path' button. After selecting a folder, the path will be 
        displayed next to the button. This directory MUST be different from the
        directory in which the original images are located.
        '''
        
        self.saveDir = QFileDialog.getExistingDirectory(self, 'Set Coded Image Folder')
        
        self.imageSaveLe.setText(self.saveDir)
        
        return self.saveDir
    
    def getImageDB(self):
        '''
        Creates a FileDialog allowing user to select an database file.
        The file should be an excel spreadsheet. The spreadsheet needs to 
        have example data in it already. Codes should be in column A, imageIDs
        in column B. Lists of Codes and imageIDs will be generated by calling 
        existingDB and a new spreadsheet name (oldDB_updated) will be specified. 
        Initiated by clicking the 'Spreadsheet File' button. After selecting
        a file the file name and file path will be displayed.
        '''
        
        imageDB = QFileDialog.getOpenFileName(self, 'Set Codes Spreadsheet')
        
        #get [0] of imageDB tuple
        imageDBPath = imageDB[0]
        dbPath, dbFile = os.path.split(imageDBPath) #splits imageDBPath to give path and file
        dbFilename, dbFileExt = dbFile.split('.') #splits dbFile to give fname and ext     
        date = dt.now().strftime('%Y%m%d')
        self.newDB = os.path.join(dbPath, dbFilename + '_' + date + '.' + dbFileExt)
        #generates new spreadsheet name
        
        self.imageDBLe.setText(dbFile)
#        self.imageDBPathLe.setText(dbPath)
        
        self.existingDB(imageDBPath)
        
        return self.newDB
        
    def existingDB(self, imageDB):
        '''
        Generates list of codes and imageIDs from an existing spreadsheet. 
        Gets input from user for spreadsheet to use.
        TODO: modify so the template can be empty
        '''

#        global DBCodes
#        global DBImages
    
        Codes = pandas.read_excel(imageDB)
        Codes.columns = ['Code', 'imageID']
        self.DBCodes = list(Codes.Code)
        self.DBImages = list(Codes.imageID)
    
#        print(DBCodes, DBImages)
        return self.DBCodes, self.DBImages
    
    def getCodeLength(self):
        '''
        Uses an InputDialog to allow user to specify the number of digits
        each code should be. A number should be entered.
        '''
        
        x, ok = QInputDialog.getInt(self, 'Code Length', 'Enter Code Length:')
        
        if ok:
            return x
        
#    def codeImages(self, imageDir, saveDir, DBCodes, DBImages):
    def codeImages(self):
        '''
        Generates a list of images from a user provided directory.
        Assigns each image a random code, while continuously 
        updating the list of codes and checking against it to prevent
        duplicate codes. Stores list of codes and image IDs in for later
        retrieval. Copies images to new user provided directory and renames
        with the assigned code.
        '''
        
        x = self.getCodeLength() #input dialog to specify code length
                

        for root, subDirs, files in os.walk(self.imageDir):
            if 'desktop.ini' in files: files.remove('desktop.ini')
            if '.DS_Store' in files: files.remove('.DS_Store')
            for i in files: 
                file_name, file_ext = i.split('.')
                while True:
                    code =str(randint(10**(x-1), 10**x-1)) #x is code length
                    if code in self.DBCodes: 
                        True
                    if code not in self.DBCodes:
                        break 
                self.DBCodes.append(code)
                self.DBImages.append(i)
                imagename = os.path.join(root, i)
                codename = os.path.join(self.saveDir, code + '.' + file_ext)
                shutil.copy2(imagename, codename)
        
        self.updateDB()
    
    
    def updateDB(self):
        '''
        Takes lists of codes and image IDs and writes them to an excel
        spreadsheet so that codes can be matched up with images later.
        The new spreadsheet is saved in the same location as the orginal spreadsheet.
        '''
        df = pandas.DataFrame({'Code' : self.DBCodes, 'imageID' : self.DBImages})
        df.to_excel(self.newDB, index=None)
        
        #display message to let user know that app is finished running
        QMessageBox.about(self, '', 'Coding is finished')

def main():
    
        app = QApplication(sys.argv)
        IC = ImageCoder()
        sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()