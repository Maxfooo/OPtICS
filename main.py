# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 14:59:58 2019

@author: MaxR
"""

### Code parser to create a matlab/numpy header file out of c++ objects 
### (structs and eventually classes)

#####################################################################
## High level view                                                  #
## --------------------------------                                 #
## 1) Gather all the files in the project                           #
## 2) Parse each file and make pythons objects                      #
## 3) Use the python objects to construct a hierarchy               #
##    (capture potential nested nature of structs)                  #
## 4) Generate the header file from the Python objects              # 
#####################################################################

import os
from FileScavenger import FileScavenger
from FileParser import FileParser
from ObjectFormatter import ObjectFormatter

if __name__ == '__main__':
    
    test_dir = "C:/Users/MaxR/Desktop/PYTHON_Workspace/OPtICS/OPtICS_Test"
    
    
    if os.name == "posix":
        top_dir = "/home/maxr/Desktop/PYTHON_Workspace/LRADS_PPP_US/src"
    else:
        top_dir = "C:/Users/MaxR/Desktop/PYTHON_Workspace/LRADS_PPP_US/src"
    
    exclude_dirs = ["bme280", "device", "gps", "memory_management", "pid", "ipc"]
    
    
    fScav = FileScavenger()
    file_list = fScav.scavenge(top_dir, exclude_dirs)
    
    print("Beginning FileParser")
    fParser = FileParser()
    objList = fParser.parseFileList(file_list)
    print("End of FileParser")
    
    objForm = ObjectFormatter()
    objList = objForm.resolveProjectHierarchy(objList)
    for o in objList:
        print(objForm.structToDtype(o))