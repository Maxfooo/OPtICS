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
        
        for objList in listOfObjLists:
            for obj in objList:
                if obj.isStruct():
                    struct_list.append(obj)
                else:
                    non_struct_list.append(obj)
                    
        for non_struct in non_struct_list:
            # see item 2) in design above
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
                        print(non_struct.getArraySizeStr())
                
        
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
                            member.setDataType(non_struct.getDataType())
                            if non_struct.isArray():
                                member.setArray()
                                member.setArraySizeStr(non_struct.getArraySizeStr())
                        
                        ##### Use struct names/typedef names to resolve member structs #####
                        # Typedef structs would have been placed as a CppObj not a CppStruct
                        # as the parser had no way to find out it was a struct yet (until now)
                        for inner_struct in struct_list:
                            if inner_struct.isTypedef():
                                inner_struct_dtype = inner_struct.getTypedefName()
                            else:
                                inner_struct_dtype = inner_struct.getDataTypeStr()
                            if member.getDataTypeStr() == inner_struct_dtype:
                                ### Need to convert this CppObject to a CppStruct
                                ### gotta make an index counter of the first 
                                ### 'struct in struct_list' item
                                s_obj = CppObject.CppStruct()
                                s_obj.setInstanceName(member.getInstanceName())
                                s_obj.setDataTypeStr(inner_struct_dtype)
                                s_obj.setDeclaration()
                                s_obj.setParentName(member.getParentName())
                                struct.exchangeMemberVar(member_index, s_obj)
                member_index += 1
        
        for s_obj in struct_list:
            s_obj.updateChildren()
        
        return struct_list
          
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
        
        if obj.isStruct():
            dtype_str += "', {0}".format(self.getStructDtypeName(obj.getDataTypeStr()))
        else:
            dtype_str += "', {0}".format(self.getDataTypeToNpType(obj.getDataTypeStr()))
            
        if obj.isArray():
            dtype_str += ", {0}".format(obj.getArraySizeStr())
        dtype_str += "),\n"
        
        return dtype_str
    
    def structToDtype(self, sObj):
        # Using Tyson's python dtype format
        if not sObj.isStruct():
            return
        s_name = self.getStructDtypeName(sObj.getDataTypeStr())
        dtype_str = s_name + " = np.dtype([\n"
        for obj in sObj.getMemberVars():
            dtype_str += self.objToDtypeMemberStr(obj)
        dtype_str += "])\n"
    
        return dtype_str
        
    def formatToMatlab(self, objList):
        return ""
    
    def formatToNumpy(self, objList):
        return ""
    
    
if __name__ == '__main__':
    
    #
    # CREATE STRUCT OBJECT
    #
    s_obj = CppObject.CppStruct()
    s_obj.setStructName("TestStruct")
    s_obj.setInstanceName("test_struct")
    
    #
    # CREATE AND ADD MEMBER VARIABLES
    #
    for i in range(4):
        c_obj = CppObject.CppObject()
        c_obj.setDataType("uint8_t")
        c_obj.setVarName(str(i))
        s_obj.addMemberVar(c_obj)
    c_obj = CppObject.CppObject()
    c_obj.setIsArray()
    c_obj.setArraySizeStr("20")
    c_obj.setDataType("float")
    c_obj.setVarName("my_array")
    s_obj.addMemberVar(c_obj)
    
    s_obj_2 = CppObject.CppStruct()
    s_obj_2.setStructName("InnerStruct")
    s_obj_2.setInstanceName("inner_struct")
    s_obj.addMemberVar(s_obj_2)
    
    #
    # FORMAT AND PRINT STUCT DTYPE
    #
    obj_form = ObjectFormatter()
    print(obj_form.structToDtype(s_obj))