# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:24:29 2019

@author: MaxR
"""

import os
from pathlib import Path

class FileScavenger(object):
    def __init__(self):
        self.files   = list()
        self.file_exts = ['.h', '.cpp', '.c']
        
    def scavenge(self, topDir=os.getcwd(), exDirs=list()):
        path = Path(topDir)
        ex_paths = self.buildExcludePaths(topDir, exDirs)
        if not (path.is_dir() and path.exists()): 
            return list()
        for x in path.iterdir():
            if (x.is_dir()):
                if x in ex_paths:
                    continue
                self.scavenge(x)
            for e in self.file_exts:
                if e in os.fspath(x):
                    self.files.append(x)
        
        return self.files
            
    def buildExcludePaths(self, topDir=os.getcwd(), exDirs=list()):
        if len(exDirs) < 1:
            return list()
        ex_paths = list()
        for f in exDirs:
            ex_dir = topDir
            if topDir[-1] != "/":
                ex_dir += "/"
            ex_dir += f
            ex_paths.append(Path(ex_dir))
        return ex_paths
            
            
if __name__ == '__main__':
    top_dir = "C:/Users/MaxR/Desktop/PYTHON_Workspace/LRADS_PPP_US/src"
    exclude_dirs = ["bme280", "device", "gps", "memory_management", "pid"]
    
    fs = FileScavenger()
    
    exDirs = fs.buildExcludePaths(top_dir, exclude_dirs)
    for e in exDirs:
        print(e)
    
    files = fs.scavenge(top_dir, exclude_dirs)
    for f in files:
        print(f)
    print(len(files))