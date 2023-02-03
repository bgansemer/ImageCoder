# Image Coder

### Version 1.1

## Building the application

This script was written in Python 3.7. The executable was compiled using Pyinstaller 5.7.0.

A standalone application was built using [Pyinstaller](https://pyinstaller.org/en/stable/).

First a spec file was generated using:

`pyi-makespec -n ImageCoder_v1.1 ImageCoderGUIv1.1.py`

Then the application was built using:

`pyinstaller ImageCoder_v1.1.spec`

The `linux/` directory contains the application built for linux (Ubuntu, WSL).

## Description

This program uses a GUI to code images (or other files). The interface allows users to 
provide a folder with images, a folder in which to save the coded images,
and an excel spreadsheet to serve as a database to keep track of images and 
their codes, allowing users to decode the images later. 
Images/files can be in any format. The image folder and 
save folder must be different from each other. The spreadsheet must be 
an excel spreadsheet. The updated spreadsheet will be saved as
'originalDB_updated'. 

To use, simply start the program by double-clicking the ImageCoder.exe file. Once the program starts a window should appear with 4 buttons and 3 lines.
You select your folders/files by clicking on each on of the buttons. The top three buttons will cause FileDialogs
to appear, allowing you to select a folder that your images (or other files to be coded) are in, a folder in 
which to save the images/files once they are coded (the save folder MUST be different from the originals folder), 
and a spreadsheet template that will be the database with image/file names and their corresponding codes that 
will allow you to break the code later. After these three things are selected, simply click the 'Code Images' button.
After clicking, a pop box will appear asking for code length in number of digits. Input a number and hit ok, and 
the program will run. Each image/file will be duplicated, and renamed with a random code, and saved to the selected
save folder. The database will be continuously updated as the program runs, allowing it to be continually checked 
to make sure no duplicate codes are used.

### Updates from version 1.0:

The folder with images in it can now have other folders! The program will walk through the entire directory tree of the provided root folder and find all images/files and code them. 

#### Other Notes:

A spreadsheet template is included in the 'templates' folder.
