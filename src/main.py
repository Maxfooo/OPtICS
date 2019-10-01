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


def main(top_dir="", exclude_dirs=[]):
    """
    Run main program
    1) Use the FileScavenger.scavenge to get all dirs in top level
        excluding the exclude dirs
    2) Use FileParser.parseFileList to parse all the files in the project
        and return a list of objects
    3) Pass the object list to ObjectFormatter.resolveProjectHierarchy 
        to properly resolve the cpp objects and values
    4) Sort the returned object list using ObjectFormatter.sortObjectHierarchy
    5) Write the sorted object list to file
    """

    fScav = FileScavenger()
    file_list = fScav.scavenge(top_dir, exclude_dirs)
    
    fParser = FileParser()
    objList = fParser.parseFileList(file_list)
    
    objForm = ObjectFormatter()
    objList = objForm.resolveProjectHierarchy(objList)
    
    objList = objForm.sortObjectHierarchy(objList, 2)
    
    objForm.objListToFile(objList)

if __name__ == '__main__':
    
    if os.name == "posix":
        top_dir = "/home/maxr/Desktop/PYTHON_Workspace/LRADS_PPP_US/src"
    else:
        top_dir = "C:/Users/MaxR/Desktop/PYTHON_Workspace/LRADS_PPP_US/src"
    
    exclude_dirs = ["bme280", "device", "memory_management", "pid", "ipc"]
    
    #
    # RUN MAIN
    #
    main(top_dir, exclude_dirs)
    
    
    
    
    
    