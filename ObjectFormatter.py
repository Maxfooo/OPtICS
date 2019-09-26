# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:36:24 2019

@author: MaxR
"""

import CppObject
import Tokens

class ObjectFormatter(object):
    def __init__(self):
        pass
    
    def resolveProjectHierarchy(self, listOfObjLists):
        ###################################################################
        # Design
        ###################################################################
        # 1) Separate objects
        #    a) Structs
        #    b) preprocessor objects and const objects
        # 2) Use (1b) list to resolve non_struct variable types to standard types
        # 3) Use (1b) list to resolve variables to numbers
        # 4) Use struct names/typedef names to resolve member structs
        # 5) Rewrite object list to reflect changes
        ###################################################################
        
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
        # GET VALUES FOR TYPEDEF'D AND CONST VARIABLE NAMES
        #
        for non_struct in non_struct_list:
            for n_struct in non_struct_list:
                if n_struct.isTypedef():
                    dtype_str = n_struct.getTypedefName()
                else:
                    dtype_str = n_struct.getInstanceName()
                if non_struct.getDataTypeStr() == dtype_str:
                    non_struct.setDataType(n_struct.getValueStr())
                    if n_struct.isArray():
                        non_struct.setArray()
                        non_struct.setArraySizeStr(n_struct.getArraySizeStr())
        
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
                
                if (self.getObjRepr(member) == member.getParentName()):
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
                    inner_struct_repr = self.getObjRepr(inner_struct)
                    if member.getDataTypeStr() == inner_struct_repr:
                        s_obj = CppObject.CppStruct()
                        s_obj.setInstanceName(member.getInstanceName())
                        s_obj.setDataTypeStr(inner_struct_repr)
                        s_obj.setDeclaration()
                        s_obj.setParentName(member.getParentName())
                        struct.exchangeMemberVar(member_index, s_obj)                           
                        
                member_index += 1

        
        #
        # REMOVE DUPLICATES
        #
        clean_struct_list = list()
        clean_struct_name_list = list()
        
        for s_obj in struct_list:
            obj_repr = self.getObjRepr(s_obj)
            if obj_repr in clean_struct_name_list:
                continue
            
            clean_struct_name_list.append(obj_repr)
            
            if s_obj.hasMemberVars():
                s_obj.updateChildren()
                
            clean_struct_list.append(s_obj)
        
        return clean_struct_list
          
    def getDataTypeToNpType(self, dataTypeStr):
        if dataTypeStr in Tokens.NpTypeMap.keys():
            return Tokens.NpTypeMap[dataTypeStr]
        else:
            return ""
              
    def getStructDtypeName(self, structName=""):
        dtype_str = structName + "_dtype"
        return dtype_str
    
    def objToDtypeMemberStr(self, obj):
        dtype_str = "  ('"
        dtype_str += obj.getInstanceName()
        s_repr = self.getObjRepr(obj)
        if obj.isStruct():
            dtype_str += "', {0}".format(self.getStructDtypeName(s_repr))
        else:
            dtype_str += "', {0}".format(self.getDataTypeToNpType(s_repr)) #obj.getDataTypeStr()))
            
        if obj.isArray():
            dtype_str += ", {0}".format(obj.getArraySizeStr())
        dtype_str += "),\n"
        
        return dtype_str
    
    def structToDtype(self, sObj):
        # Using Tyson's python dtype format
        if not sObj.isStruct():
            return
        s_name = self.getStructDtypeName(self.getObjRepr(sObj))
        dtype_str = s_name + " = np.dtype([\n"
        for obj in sObj.getMemberVars():
            dtype_str += self.objToDtypeMemberStr(obj)
        dtype_str += "])\n"
    
        return dtype_str
        
    def getObjRepr(self, obj):
        if obj.isTypedef():
            return obj.getTypedefName()
        else:
            return obj.getDataTypeStr()
    
    def objListToFile(self, objList, filename="Numpy_Dtype.txt"):
        # Clear contents of file if it exists
        f = open(filename, 'w')
        f.write("")
        f.close()
        # Write dtypes to file
        f = open(filename, 'a')
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
    
    test = [1,2,3,4]
    new_test = list()
    print(test)
    for x in test:
        x += 1
        new_test.append(x)
    test = new_test
    print(test)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    