# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:36:24 2019

@author: MaxR
"""


import CppObject
import Tokens
from itertools import chain

class ObjectFormatter(object):
    def __init__(self):
        pass
    
    def resolveProjectHierarchy(self, listOfObjLists):
        """
        -------------------------------------------------------------------
        # Design
        -------------------------------------------------------------------
        # 1) Separate objects
        #    a) Structs
        #    b) preprocessor objects and const objects
        # 2) Use (1b) list to resolve non_struct variable types to standard types
        # 3) Use (1b) list to resolve variables to numbers
        # 4) Use struct names/typedef names to resolve member structs
        # 5) Rewrite object list to reflect changes
        -------------------------------------------------------------------
        """
        
        struct_list = list()
        non_struct_list = list()
        
        #
        # SPLIT STRUCTS AND NON STRUCTS
        #
        for objList in listOfObjLists:
            for obj in objList:
                if obj.isStruct():
                    struct_list.append(obj)
                else:
                    non_struct_list.append(obj)
        
        #
        # GET VALUES FOR TYPEDEF'D, CONST, AND #DEFINED VARIABLE NAMES
        #
        for non_struct in non_struct_list:
            for n_struct in non_struct_list:
                if n_struct.isTypedef():
                    dtype_str = n_struct.getTypedefName()
                else:
                    dtype_str = n_struct.getInstanceName()
                    
                if non_struct.getDataTypeStr() == dtype_str:
                    non_struct.setDataTypeStr(n_struct.getValueStr())
                    if n_struct.isArray():
                        non_struct.setArray()
                        non_struct.setArraySizeStr(n_struct.getArraySizeStr())
                        non_struct.setIs2dArray(n_struct.is2dArray())
                        non_struct.setArray2dSizeStr(n_struct.getArray2dSizeStr())
                    break
        #
        # RESOLVE MEMBER VARIABLE VALUES, NAMES, AND STRUCTS
        #
        for struct in struct_list:
            member_index = 0
            for member in struct.getMemberVars():
                
                # Need to check
                # 1) array size str
                # 2) variable data types (replace typedef with standard data type)
                # 3) if member data type matches a struct, swap CppObject from CppStruct
                
                for non_struct in non_struct_list:
                    
                    
                    ##### Exchange Array Size Var with Number #####
                    if member.isArray():
                        if non_struct.isTypedef():
                            non_struct_str = non_struct.getTypedefName()
                        else:
                            non_struct_str = non_struct.getInstanceName()
                        if member.getArraySizeStr() == non_struct_str:
                            member.setArraySizeStr(non_struct.getValueStr())
                        if member.getArray2dSizeStr() == non_struct_str:
                            member.setArray2dSizeStr(non_struct.getValueStr())
                            
                    
                    if not member.isStruct():
                        ##### Exchange Alternative Data Types with Standard Data Types #####
                        # The exact thing as the for loop I did for item 2) lol
                        if non_struct.isTypedef():
                            dtype_str = non_struct.getTypedefName()
                        else:
                            dtype_str = non_struct.getInstanceName()
                        if member.getDataTypeStr() == dtype_str:
                            member.setDataTypeStr(non_struct.getDataTypeStr())
                            if non_struct.isArray():
                                member.setArray()
                                member.setArraySizeStr(non_struct.getArraySizeStr())
                
                if (CppObject.getObjRepr(member) == member.getParentName()):
                    # need to delete this member var because it
                    # is itself within in its own definition
                    # (don't want an infinite struct within itself)
                    struct.removeMemberVar(member_index)
                    member_index += 1
                    continue
                
                ##### Use struct names/typedef names to resolve member structs #####
                # Typedef structs would have been placed as a CppObj not a CppStruct
                # as the parser had no way to find out it was a struct yet (until now)
                for inner_struct in struct_list:
                    inner_struct_repr = CppObject.getObjRepr(inner_struct)
                    if member.getDataTypeStr() == inner_struct_repr:
                        s_obj = CppObject.CppStruct()
                        s_obj.setInstanceName(member.getInstanceName())
                        s_obj.setDataTypeStr(inner_struct_repr)
                        s_obj.setDeclaration()
                        s_obj.setParentName(member.getParentName())
                        if member.isArray():
                            s_obj.setArray()
                            s_obj.setArraySizeStr(member.getArraySizeStr())
                            s_obj.setIs2dArray(member.is2dArray())
                            s_obj.setArray2dSizeStr(member.getArray2dSizeStr())
                        struct.exchangeMemberVar(member_index, s_obj)
                        
                member_index += 1

        
        #
        # REMOVE DUPLICATES
        #
        clean_struct_list = list()
        clean_struct_name_list = list()
        
        for s_obj in struct_list:
            obj_repr = CppObject.getObjRepr(s_obj)
            if obj_repr in clean_struct_name_list:
                continue
            
            clean_struct_name_list.append(obj_repr)
            
            if s_obj.hasMemberVars():
                s_obj.updateChildren()
                
            clean_struct_list.append(s_obj)
        
        return clean_struct_list
          
    def getDataTypeToNpType(self, dataTypeStr):
        """
        Using Tokens.NpTypeMap dictionary, convert cpp data types to the
            numpy dtype representation
        Ex. int8_t --> np.int8
        """
        if dataTypeStr in Tokens.NpTypeMap.keys():
            return Tokens.NpTypeMap[dataTypeStr]
        else:
            return ""
              
    def getStructDtypeName(self, structName=""):
        """
        Simply append '_dtype' to the end of the struct name
        This keeps struct names consistent
        """
        dtype_str = structName + "_dtype"
        return dtype_str
    
    def objToDtypeMemberStr(self, obj):
        """
        Take the essential properties of a cpp object and make it
            a member description for a dtype definition
        Ex. 'int8_t my_arr[3];' --> obj
            obj --> ('my_arr', np.int8, 3),
        """
        has_dtype = True
        dtype_str = "  ('"
        dtype_str += obj.getInstanceName()
        s_repr = CppObject.getObjRepr(obj)
        if obj.isStruct():
            member_repr = self.getStructDtypeName(s_repr)
        else:
            member_repr = self.getDataTypeToNpType(s_repr)
            
        if not member_repr:
            has_dtype = False
            
        dtype_str += "', {0}".format(member_repr)
            
        if obj.isArray():
            dtype_str += ", {0}".format(obj.getArraySizeStr())
            if obj.is2dArray():
                dtype_str += " * {0}".format(obj.getArray2dSizeStr())
        dtype_str += "),\n"
        
        return dtype_str, has_dtype
    
    def structToDtype(self, sObj):
        """
        Build a numpy dtype definition from a struct object.
        A header will be created with the struct name and each of it's 
            member variables will be converted into a dtype member string
            and placed in this definition string.
        """
        block_comment = False
        # Using Tyson's python dtype format
        if not sObj.isStruct():
            return
        s_name = self.getStructDtypeName(CppObject.getObjRepr(sObj))        
        dtype_str = s_name + " = np.dtype([\n"
        for obj in sObj.getMemberVars():
            d_str, has_dtype = self.objToDtypeMemberStr(obj)
            dtype_str += d_str
            if not has_dtype:
                block_comment = True
        dtype_str += "])\n"
    
        # check if all the members have data types, if not, comment the dtype block
        if block_comment:
            copy_dtype_str = dtype_str
            dtype_str = '"""\n' + copy_dtype_str + '"""\n'
    
        return dtype_str
    
    def sortObjectHierarchy(self, structList, runCount=1):
        """ 
        Sort the list of objects such that all dependent (inner) struct
        are listed first. 
        An optional parameter 'runCount' lets the user recursively call
            this function 2-4 times, the reason is as follows:
        Several parent structs can have the same child struct and be placed out of order.
        Ex.
            -----------
            Paremeters:
            -----------
            Struct A has child struct B, and struct B has a child C 
            Struct D has child C
            The list of struct A-D is initially random
            ----------------------
            Problematic Situation:
            ----------------------
            1) Struct A is appended to the sorted list (no dependencies yet)
            2) Struct D is appended to the sorted list (no dependencies yet)
            3) Struct C is inserted in the sorted list
                a) Because C is a child of D, it is inserted in front of D (after struct A)
            4) Struct B is inserted in the sorted list
                a) Because B is a child of A, it is inserted in front of A
                b) Because A is in front of C, and B is in front of A, 
                    C, the child of B, is now defined AFTER B, which will cause a PROBLEM
        """
        
        n = len(structList)
        
        if n < 1:
            return structList
        
        sorted_list = list()
        inserted = False
        
        
        
        for s in range(n):
            if s == 0:
                sorted_list.append(structList[s])
            else:
                inserted = False
                for ss in range(len(sorted_list)):
                    possible_child_repr = CppObject.getObjRepr(structList[s])
                    child_repr_list = sorted_list[ss].getMemberVarReprs()
                    
                    if possible_child_repr in child_repr_list:
                        if ss == 0:
                            sorted_list.insert(0, structList[s])
                        else:
                            sorted_list.insert(ss-1, structList[s])
                        inserted = True
                        break
                
                if not inserted:
                    sorted_list.append(structList[s])
                    
                    
        if runCount > 1 and runCount < 5:
            runCount -= 1
            sorted_list = self.sortObjectHierarchy(sorted_list, runCount)
            
        return sorted_list
    
    def objListToFile(self, objList, filename="OPtICS_dtypes.py"):
        """
        Iterate through a list of objects and create dtype definitions for all of
            them, then write those strings to file.
        The file WILL OVERWRITE previous files with the same name.
        """
        # Clear contents of file if it exists
        f = open(filename, 'w')
        f.write("")
        f.close()
        # Write dtypes to file
        f = open(filename, 'a')
        f.write("import numpy as np\n\n")
        for obj in objList:
            f.write(self.structToDtype(obj))
            f.write("\n")
            
        f.close()
    
    
if __name__ == '__main__':
    
    #
    # CREATE STRUCT OBJECT
    #
    s_obj = CppObject.CppStruct()
    s_obj.setDataTypeStr("TestStruct")
    s_obj.setInstanceName("test_struct")
    
    #
    # CREATE AND ADD MEMBER VARIABLES
    #
    for i in range(4):
        c_obj = CppObject.CppObject()
        c_obj.setDataTypeStr("uint8_t")
        c_obj.setInstanceName(str(i))
        s_obj.addMemberVar(c_obj)
    c_obj = CppObject.CppObject()
    c_obj.setArray()
    c_obj.setArraySizeStr("20")
    c_obj.setDataTypeStr("float")
    c_obj.setInstanceName("my_array")
    s_obj.addMemberVar(c_obj)
    
    s_obj_2 = CppObject.CppStruct()
    s_obj_2.setDataTypeStr("InnerStruct")
    s_obj_2.setInstanceName("inner_struct")
    s_obj.addMemberVar(s_obj_2)
    
    #
    # FORMAT AND PRINT STUCT DTYPE
    #
    obj_form = ObjectFormatter()
    print(obj_form.structToDtype(s_obj))
    
    
    #
    #
    #
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    