# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:11:42 2019

@author: MaxR
"""

def getObjRepr(obj):
    if obj.isTypedef():
        return obj.getTypedefName()
    else:
        return obj.getDataTypeStr()

class CppObject(object):
    def __init__(self):
        self.is_empty          = False
        self.is_array          = False
        self.is_2d_array       = False
        self.is_struct         = False
        self.is_typedef        = False
        self.str_data_type     = ""
        self.str_instance_name = ""
        self.str_typedef_name  = ""
        self.str_array_size    = ""
        self.str_array_2d_size = ""
        self.str_parent_name   = ""
        
    #
    # IS EMPTY
    #
    def setIsEmpty(self, isEmpty):
        self.is_empty = isEmpty
    def setEmpty(self):
        self.is_empty = True
    def unsetEmpty(self):
        self.is_empty = False
    def isEmpty(self):
        return self.is_empty
    
    #
    # IS ARRAY
    #
    def setIsArray(self, isArray):
        self.is_array = isArray
    def setArray(self):
        self.is_array = True
    def unsetArray(self):
        self.is_array = False
    def isArray(self):
        return self.is_array
        
    #
    # IS 2D ARRAY
    #
    def setIs2dArray(self, is2dArray):
        self.is_2d_array = is2dArray
    def set2dArray(self):
        self.is_2d_array = True
    def reset2dArray(self):
        self.is_2d_array = False
    def is2dArray(self):
        return self.is_2d_array
    
    
    #
    # IS STRUCT
    #
    def setIsStruct(self, isStruct):
        self.is_struct = isStruct
    def setStruct(self):
        self.is_struct = True
    def unsetIsStruct(self):
        self.is_struct = False
    def isStruct(self):
        return self.is_struct
    
    #
    # IS TYPEDEF
    #
    def setIsTypedef(self, isTypedef):
        self.is_typedef = isTypedef
    def setTypedef(self):
        self.is_typedef = True
    def unsetTypedef(self):
        self.is_typedef = False
    def isTypedef(self):
        return self.is_typedef
    
    #
    # DATA TYPE
    #
    def setDataTypeStr(self, dType=""):
        self.str_data_type = dType
    def getDataTypeStr(self):
        return self.str_data_type
    
    #
    # INSTANCE NAME
    #
    def setInstanceName(self, iName=""):
        self.str_instance_name = iName
    def getInstanceName(self):
        return self.str_instance_name
        
    #
    # TYPEDEF NAME
    #
    def setTypedefName(self, tName=""):
        self.str_typedef_name = tName
    def getTypedefName(self):
        return self.str_typedef_name
        
    #
    # ARRAY SIZE
    #
    def setArraySizeStr(self, aSize=""):
        self.str_array_size = aSize
    def getArraySizeStr(self):
        return self.str_array_size
    
    #
    # ARRAY 2D SIZE
    #
    def setArray2dSizeStr(self, a2dSize=""):
        self.str_array_2d_size = a2dSize
    def getArray2dSizeStr(self):
        return self.str_array_2d_size
    
    #
    # PARENT NAME
    #
    def setParentName(self, pName=""):
        self.str_parent_name = pName
    def getParentName(self):
        return self.str_parent_name
    
    #
    # REPRESENT
    #
    def represent(self):
        repr_str = """
                    Is Empty:........ {0}
                    Is Array:........ {1}
                    Is 2D Array:..... {2}
                    Is Struct:....... {3}
                    Is Typedef:...... {4}
                    Data Type:....... {5}
                    Instance Name:... {6}
                    Typedef Name:.... {7}
                    Array Size:...... {8}
                    Array 2D Size:... {9}
                    Parent Name:..... {10}
        """.format( self.is_empty, \
                    self.is_array, \
                    self.is_2d_array, \
                    self.is_struct, \
                    self.is_typedef, \
                    self.str_data_type, \
                    self.str_instance_name, \
                    self.str_typedef_name, \
                    self.str_array_size, \
                    self.str_array_2d_size, \
                    self.str_parent_name)
        
        return repr_str
    
    def __repr__(self):
        return self.represent()

class CppUnit(CppObject):
    def __init__(self):
        CppObject.__init__(self)
        self.is_define        = False
        self.is_constexpr     = False
        self.is_const         = False
        self.is_enum          = False
        self.str_value        = ""
        
    #
    # IS DEFINE
    #
    def setIsDefine(self, isDefine):
        self.is_define = isDefine
    def setDefine(self):
        self.is_define = True
    def unsetDefine(self):
        self.is_define = False
    def isDefine(self):
        return self.is_define
    
    #
    # IS CONSTEXPR
    #
    def setIsConstexpr(self, isConstexpr):
        self.is_constexpr = isConstexpr
    def setConstexpr(self):
        self.is_constexpr = True
    def unsetConstexpr(self):
        self.is_constexpr = False
    def isConstexpr(self):
        return self.is_constexpr
    
    #
    # IS CONST
    #
    def setIsConst(self, isConst):
        self.is_const = isConst
    def setConst(self):
        self.is_const = True
    def unsetConst(self):
        self.is_const = False
    def isConst(self):
        return self.is_const
        
    #
    # IS ENUM
    #
    def setIsEnum(self, isEnum):
        self.is_enum = isEnum
    def setEnum(self):
        self.is_enum = True
    def resetEnum(self):
        self.is_enum = False
    def isEnum(self):
        return self.is_enum
    
    #
    # VALUE
    #
    def setValueStr(self, val=""):
        self.str_value = val
    def getValueStr(self):
        return self.str_value
    
    
    #
    # REPRESENT
    #
    def __repr__(self):
        repr_str = self.represent()
        repr_str += """
                    Is Define:...... {0}
                    Is Constexpr:... {1}
                    Is Const:....... {2}
                    Value:.......... {3}
        """.format( self.is_define, \
                    self.is_constexpr, \
                    self.is_const, \
                    self.str_value)
        
        return repr_str
    

class CppStruct(CppObject):
    def __init__(self):
        CppObject.__init__(self)
        self.is_declaration   = False
        self.member_vars      = list()
        self.member_var_reprs = list()
        self.nested_structs   = list()
        self.setStruct()
        
    #
    # IS DECLARATION
    #
    def setIsDeclaration(self, isDeclaration):
        self.is_declaration = isDeclaration
    def setDeclaration(self):
        self.is_declaration = True
    def unsetIsDeclaration(self):
        self.is_declaration = False
    def isDeclaration(self):
        return self.is_declaration
            
    #
    # MEMBER VARS
    #
    def addMemberVar(self, member):
        if self.is_typedef:
            member.setParentName(self.str_typedef_name)
        else:
            member.setParentName(self.str_data_type)
        self.member_vars.append(member)
        self.member_var_reprs.append(getObjRepr(member))
    def getMemberVars(self):
        return self.member_vars
    def removeMemberVar(self, index):
        if (index >= len(self.member_vars)):
            return
        del self.member_var_reprs[index]
        del self.member_vars[index]
    def removeMemberVarObj(self, member):
        self.member_var_reprs.remove(getObjRepr(member))
        self.member_vars.remove(member)
    def insertMemberVar(self, index, member):
        self.member_var_reprs.insert(index, getObjRepr(member))
        self.member_vars.insert(index, member)
    def exchangeMemberVar(self, index, newMember):
        if (index >= len(self.member_vars)):
            return
        self.member_var_reprs[index] = getObjRepr(newMember)
        self.member_vars[index] = newMember
    def hasMemberVars(self):
        return ( len(self.member_vars) > 0 )
    
    #
    # MEMBER VAR REPRS
    #
    def getMemberVarReprs(self):
        return self.member_var_reprs
    
    #
    # NESTED STRUCT (struct defined within this struct)
    #
    def addNestedStruct(self, nStruct):
        if self.is_typedef:
            nStruct.setParentName(self.str_typedef_name)
        else:
            nStruct.setParentName(self.str_data_type)
        self.nested_structs.append(nStruct)
    def getNestedStructs(self):
        return self.nested_structs
    
    #
    # UPDATE CHILDREN
    #
    def updateChildren(self):
        parent_str = ""
        if self.is_typedef:
            parent_str = self.str_typedef_name
        else:
            parent_str = self.str_data_type
            
        for m in self.member_vars:
            m.setParentName(parent_str)
        
        for n in self.nested_structs:
            n.setParentName(parent_str)
    
    #
    # MEMBERS HAVE DTYPES?
    # 
    def membersHaveDtypes(self):
        for m in self.member_vars:
            if len(m.getDataTypeStr()) < 1:
                return False
        return True
    
    #
    # REPRESENT
    #
    def __repr__(self):
        repr_str = self.represent()
        repr_str += """
                    Is Declaration:...... {0}
                    Has Member Vars:..... {1}
                    Has Nested Struct:... {2}
        """.format( self.is_declaration, \
                    len(self.member_vars) > 0, \
                    len(self.nested_structs) > 0)
        
        return repr_str
