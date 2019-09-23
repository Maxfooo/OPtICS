# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:13:43 2019

@author: MaxR
"""

import re

def cleanReFindallList(findallList):
    """
    findallList = re.findall(regex, str)
    remove from list:
        1) empty entries
        2) duplicate entries
    """
    if len(findallList) < 1: 
        return list()
    
    dupe = False
    tidy_list = list()
    for match in findallList:
        tidy_tuple = list()
        for m in match:
            m = m.strip()
            if m == '': 
                continue
            if len(tidy_tuple) > 0:
                for t in tidy_tuple:
                    if m == t: 
                        dupe = True
                        continue
            if dupe:
                dupe = False
                continue
            else:
                tidy_tuple.append(m)                
        
        if len(tidy_tuple) >= 1:
            tidy_list.append(tuple(tidy_tuple))
        
    return tidy_list

def regexFindall(regex, target):
    """
    Uses re.findall(regex, target) and automatically
        passes it through the 'cleanReFindallList() functions
    returns resulting list
    """
    findall_list = re.findall(regex, target)
    return cleanReFindallList(findall_list)

def arrSizeFromCSV(csv_str):
    """
    arrays can be declared with out an explicit size, such as
        uint8_t my_array[] = {1, 2, 3, 4};
    return the size of the list made from spliting the string
        containing the CSV
    """
    return len(csv_str.split(","))
    
    
    
    
    
    
    
    