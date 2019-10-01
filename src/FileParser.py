# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:06:09 2019

@author: MaxR
"""

import CppObject
#from CppObject import getObjRepr
import Tokens
import Utils

print_found_objects = False

class FileParser(object):
    """
    Will take .c .cpp and .h files and parse them
        for their contents. Contents include structs, unions, 
        constants (const, constexpr, #define) and typedefs.
    The contents will then be made into objects,
        put into a list and the user can do what they want.
    """
    def __init__(self):
        """
        Initialize class variables including an instance of the Tokens class
        """
        self.obj_list = list()
        self.code_reg = Tokens.CodeRegex()
        self.current_file_name = ""
        self.current_line_num = 0
        
    def parseFileList(self, fileList):
        """
        Take list of file names and run all of them through the
            'parseFile' function
        """
        for f in fileList:
            
            self.obj_list.append(self.parseFile(f))
        return self.obj_list
    
    def parseFile(self, file):
        """
        Implementation of the class description. 
        Parse file for Cpp objects.
        """
        self.current_file_name = file
        
        print(file)
        
        obj_list = list()
        
        making_struct = False
        s_obj_q = list()
        s_obj_q_index = 0
        
        block_comment = False
        
        self.current_line_num = 0
        
        with open(file) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()
                
                
                self.current_line_num += 1
                #print(self.current_line_num)
                
                ########################################################
                # Check for specific keywords we don't want/care about #
                ########################################################
                match_list = Utils.regexFindall(self.code_reg.getAvoidRegex(), line)
                if len(match_list) > 0:
                    if "*/" in match_list[0] or "*/" in line:
                        block_comment = False
                    continue
                
                ################################
                # Check for commented out code #
                ################################
                # '//' single line comments are in the avoid regex
                            
                if "/*" in line:
                    block_comment = True
                    continue
                if "*/" in line:
                    block_comment = False
                    continue
                if block_comment:
                    continue
                
                ##################################
                # There is a priority to parsing #
                ##################################
                # 1) Structs                     #
                # 2) Preproc keywords & const    #
                # 3) Variables & arrays          #
                ##################################
                
                
                ### Struct ### (Unions will be treated very similarly to structs)
                # 1) Struct head
                # 1b) If struct header does NOT match, move on to preprocessor
                # 2) Gather contents of struct until a Struct Tail match
                # 3) Make CppStruct object for struct
                # 4) Make CppObject for struct members, making sure to mark any member structs
                
                
                if making_struct:
                    #
                    # Check for end of struct
                    #
                    match_list = Utils.regexFindall(self.code_reg.getStructTailRegex(), line)
                    if len(match_list) > 0:
                        self.finishStructObj(match_list, s_obj_q[s_obj_q_index-1])
                        s_obj_q_index -= 1
                        s_obj = s_obj_q.pop()
                        if s_obj_q_index >= 1:
                            if not s_obj.isEmpty():
                                s_obj_q[s_obj_q_index-1].addNestedStruct(s_obj)
                        else:
                            if not s_obj.isEmpty():
                                obj_list.append(s_obj)
                            making_struct = False
                        continue
                
                match_list = Utils.regexFindall(self.code_reg.getStructHeadRegex(), line)
                if len(match_list) < 1:
                    match_list = Utils.regexFindall(self.code_reg.getUnionHeadRegex(), line)
                    
                if len(match_list) > 0:
                    s_obj = self.startStructObj(match_list)
                    
                    if s_obj.isDeclaration():
                        if making_struct:
                            s_obj_q[s_obj_q_index-1].addMemberVar(s_obj)
                        else:
                            obj_list.append(s_obj)
                    else:
                        making_struct = True
                        s_obj_q.append(s_obj)
                        s_obj_q_index += 1
                        
                    continue
                
                ### Preprocessor objs ###
                
                #
                # #define
                #
                match_list = Utils.regexFindall(self.code_reg.getDefineRegex(), line)
                if len(match_list) > 0:
                    unit_obj = self.makeDefineObj(match_list)
                    if unit_obj.isEmpty():
                        continue
                    if print_found_objects:
                        print("Found #define")
                        print(match_list)
                    obj_list.append(unit_obj)
                    continue
                    
                
                #
                # constexpr
                #
                match_list = Utils.regexFindall(self.code_reg.getConstexprRegex(), line)
                if len(match_list) > 0:
                    cpp_obj = self.makeConstexprObj(match_list)
                    if cpp_obj.isEmpty():
                        continue
                    if print_found_objects:
                        print("Found constexpr")
                        print(match_list)
                    obj_list.append(cpp_obj)
                    continue
                
                #
                # typedef
                #
                match_list = Utils.regexFindall(self.code_reg.getTypedefRegex(), line)
                if len(match_list) > 0:
                    cpp_obj = self.makeTypedefObj(match_list)
                    if cpp_obj.isEmpty():
                        continue
                    if print_found_objects:
                        print("Found typedef")
                        print(match_list)
                    obj_list.append(cpp_obj)
                    continue
                
                ### Variables ###
                
                #
                # Arrays
                #
                match_list = Utils.regexFindall(self.code_reg.getArrayRegex(), line)
                if len(match_list) > 0:
                    cpp_obj = self.makeArrayObj(match_list)
                    
                    if cpp_obj.isEmpty():
                        continue
                    
                    if (making_struct):
                        s_obj_q[s_obj_q_index-1].addMemberVar(cpp_obj)
                        if print_found_objects:
                            print("Found array")
                            print(match_list)
                    continue
                
                #
                # 2D Arrays
                #
                match_list = Utils.regexFindall(self.code_reg.get2dArrayRegex(), line)
                if len(match_list) > 0:
                    cpp_obj = self.make2dArrayObj(match_list)
                    
                    if cpp_obj.isEmpty():
                        continue
                    
                    if (making_struct):
                        s_obj_q[s_obj_q_index-1].addMemberVar(cpp_obj)
                        if print_found_objects:
                            print("Found 2D array")
                            print(match_list)
                    continue
                
                #
                # Variables
                #
                match_list = Utils.regexFindall(self.code_reg.getVariableRegex(), line)
                if len(match_list) > 0:
                    cpp_obj = self.makeVarObj(match_list)
                    
                    if cpp_obj.isEmpty():
                        continue
                    
                    if (making_struct):
                        s_obj_q[s_obj_q_index-1].addMemberVar(cpp_obj)
                        if print_found_objects:
                            print("Found variable")
                            print(match_list)
                    else:
                        if cpp_obj.isConst():
                            obj_list.append(cpp_obj)
                            if print_found_objects:
                                print("Found variable")
                                print(match_list)
                            
                    continue
                
                match_list = Utils.regexFindall(self.code_reg.getEnumRegex(), line)
                if len(match_list) > 0:
                    cpp_obj = self.makeEnumObj(match_list)
                    
                    if cpp_obj.isEmpty():
                        continue
                    
                    if (making_struct):
                        s_obj_q[s_obj_q_index-1].addMemberVar(cpp_obj)
                        if print_found_objects:
                            print("Found enum")
                            print(match_list)
                    else:
                        obj_list.append(cpp_obj)
                        if print_found_objects:
                            print("Found enum")
                            print(match_list)
                            
                    continue
                        
                    
                
                
        for o in obj_list:
            if o.isStruct():
                o.updateChildren()      
                if (not o.getDataTypeStr() and not o.getTypedefName()):
                    print("Found empty data type struct")
                    print(o)
                    mem = o.getMemberVars()
                    for m in range(len(mem)):
                        if m > 2:
                            break
                        print("Member")
                        print(mem[m])
                        
                        
        return obj_list
    
    """
    STRUCT (UNION) START
    """
    def startStructObj(self, structMatchList):
        """
        structs are usually multiline definitions, there for check the 
            first line a struct is declared (or possibly instantiated)
            and begin an object to be filled with member variables 
            (which could include another struct)
        """
        s_obj = CppObject.CppStruct()
        
        if len(structMatchList) < 1:
            s_obj.setEmptyObj()
            return s_obj
        
        s_tuple = structMatchList[0]
        
        if len(s_tuple) < 2:
            s_obj.setEmpty()
            return s_obj
        
        if Tokens.PreProcessor[2] in s_tuple:
            s_obj.setTypedef()
        else:
            s_obj.setDataTypeStr(s_tuple[1])
        
        if ";" in s_tuple:
            decl_token = s_tuple.index(";")
            s_obj.setDeclaration()
            s_obj.setInstanceName(s_tuple[2])
            if not s_obj.isTypedef():
                if len(s_tuple) > 3 and decl_token != 3:
                    s_obj.setArray()
                    s_obj.setArraySizeStr(s_tuple[3])
        
        return s_obj
    
    """
    STRUCT (UNION) END
    """
    def finishStructObj(self, structMatchList, s_obj):
        """
        As structs are usually multiline definitions, this function
            is called when the end of the struct def is matched and
            checks for completion, an instance name or possibly a typedef name.
        """
        if len(structMatchList) < 1:
            return s_obj
        
        s_tuple = structMatchList[0];
        
        if len(s_tuple) == 2:
            if "(" in s_tuple[1]:
                return s_obj
            name_str = s_tuple[1]
        elif (len(s_tuple) == 3):
            name_str = s_tuple[2]
        else:
            return s_obj
            
        
        if s_obj.isTypedef():
            s_obj.setTypedefName(name_str)
        else:
            s_obj.setInstanceName(name_str)
        
        return s_obj
    
    """
    DEFINE
    """
    def makeDefineObj(self, matchList):
        """
        Make an object specific for a defined value in cpp
        This will later be used to swap names out for values
        """
        u_obj = CppObject.CppUnit()
        
        if len(matchList) < 1:
            u_obj.setEmpty()
            return u_obj
        
        obj_tuple = matchList[0]
        if len(obj_tuple) < 3:
            u_obj.setEmpty()
            return u_obj
        
        u_obj.setDefine()
        u_obj.setInstanceName(obj_tuple[1])
        u_obj.setValueStr(obj_tuple[2])
        return u_obj
    
    """
    CONSTEXPR
    """
    def makeConstexprObj(self, matchList):
        """
        Make an object specific for constexpr value in cpp
        This will later be used to swap names out for values
        """
        u_obj = CppObject.CppUnit()
        
        if len(matchList) < 1:
            u_obj.setEmpty()
            return u_obj
        
        obj_tuple = matchList[0]
        if len(obj_tuple) < 4:
            u_obj.setEmpty()
            return u_obj
        
        u_obj.setConstexpr()
        u_obj.setDataTypeStr(obj_tuple[1])
        u_obj.setInstanceName(obj_tuple[2])
        u_obj.setValueStr(obj_tuple[3])
        return u_obj
    
    """
    TYPEDEF
    """
    def makeTypedefObj(self, matchList):
        """
        Make an object specific for typedef value in cpp
        This will later be used to swap names out for base data types in cpp
            as well as exchange typedef'd member variable objects into
            struct objects.
        """
        u_obj = CppObject.CppUnit()
        
        if len(matchList) < 1:
            u_obj.setEmpty()
            return u_obj
        
        obj_tuple = matchList[0]
        if len(obj_tuple) < 3:
            u_obj.setEmpty()
            return u_obj
        
        u_obj.setTypedef()
        u_obj.setDataTypeStr(obj_tuple[1])
        u_obj.setTypedefName(obj_tuple[2])
        if len(obj_tuple) > 3:
            u_obj.setArray()
            u_obj.setArraySizeStr(obj_tuple[3])
        
        return u_obj
    
    """
    ARRAY
    """
    def makeArrayObj(self, matchList):
        """
        Make an object specific for arrays in cpp
        This object will include a data type, instance name, and array size
        If array size is not given (in the case of initialized arrays at compile time)
            then it will be calculated automatically based on the initial array decaration
            (ex. uint8_t my_array[] = {1, 2, 3};)
            The size is 3
        """
        u_obj = CppObject.CppUnit()
        
        if len(matchList) < 1:
            u_obj.setEmpty()
            return u_obj
        
        obj_tuple = matchList[0]
        if len(obj_tuple) < 4:
            u_obj.setEmpty()
            return u_obj
        
        for o in obj_tuple:
            if "[" in o:
                u_obj.setArray()
                break
            
        if not u_obj.isArray():
            u_obj.setEmpty()
            return u_obj
        
        index = 0
        if len(obj_tuple) > 4:
            index = 1
            
        u_obj.setDataTypeStr(obj_tuple[index])
        index += 1
        u_obj.setInstanceName(obj_tuple[index])
        index += 1
        if obj_tuple[index] == "[]":
            index += 1
            u_obj.setArraySizeStr(str(Utils.arrSizeFromCSV(obj_tuple[index])))
        else:
            index += 1
            u_obj.setArraySizeStr(obj_tuple[index])           
        
        return u_obj
    
    """
    2D ARRAY
    """
    def make2dArrayObj(self, matchList):
        """
        Make object specific for 2 dimensional arrays in cpp
        This object will include a data type, instance name, and sizes for the array
        This object will, however, NOT automatically determine the size of the 2d
            from an initialized 2d array.
        @todo Add support for initialized 2d arrays (calculate size based on init)
        """
        u_obj = CppObject.CppUnit()
        
        if len(matchList) < 1:
            u_obj.setEmpty()
            return u_obj
        
        obj_tuple = matchList[0]
        if len(obj_tuple) < 3:
            u_obj.setEmpty()
            return u_obj
        
        u_obj.setArray()
        u_obj.set2dArray()
        u_obj.setDataTypeStr(obj_tuple[0])
        u_obj.setInstanceName(obj_tuple[1])
        u_obj.setArraySizeStr(obj_tuple[2])
        
        if len(obj_tuple) == 4:
            u_obj.setArray2dSizeStr(obj_tuple[3])
        elif len(obj_tuple) == 3:
            # if row == column, re.findall only catches 1 instance
            u_obj.setArray2dSizeStr(obj_tuple[2]) 
        elif len(obj_tuple) == 5:
            if obj_tuple[0] == Tokens.TYPEDEF:
                u_obj.setTypedef()
            u_obj.setDataTypeStr(obj_tuple[1])
            u_obj.setTypedefName(obj_tuple[2])
            u_obj.setArraySizeStr(obj_tuple[3])
            u_obj.setArray2dSizeStr(obj_tuple[4])
        else:
            u_obj.setEmpty()       
        
        return u_obj
    
    """
    VARIABLE
    """
    def makeVarObj(self, matchList):
        """
        Make object specific for a variable in cpp
        This object will include, at minimum, a data type and instance name
        If the variable is initialized, the object will include the init value
        """
        u_obj = CppObject.CppUnit()
        
        if len(matchList) < 1:
            u_obj.setEmpty()
            return u_obj
        
        obj_tuple = matchList[0]
        if len(obj_tuple) < 2:
            u_obj.setEmpty()
            return u_obj
        
        if "return" in obj_tuple:
            u_obj.setEmpty()
            return u_obj
        
        if ":" in obj_tuple: # bit field bit
            u_obj.setEmpty()
            return u_obj
        
        index = 0
        if obj_tuple[0] in Tokens.Qualifiers:
            if obj_tuple[0] == Tokens.Qualifiers[0]:
                u_obj.setConst()
            index = 1
            
        
        u_obj.setDataTypeStr(obj_tuple[index])
        index += 1
        u_obj.setInstanceName(obj_tuple[index])
        index += 1
        if len(obj_tuple) > 3:
            u_obj.setValueStr(obj_tuple[index])
        
        try:
            float(u_obj.getInstanceName())
            u_obj.setEmpty()
            return u_obj
        except:
            pass
        
        return u_obj
        
    """
    ENUM
    """
    def makeEnumObj(self, matchList):
        """
        Make object specific for [typedef] enum in cpp
        The data type is assumed to be an int32_t
        """
        u_obj = CppObject.CppUnit()
        
        
        if len(matchList) < 1:
            u_obj.setEmpty()
            return u_obj
        
        obj_tuple = matchList[0]
        if len(obj_tuple) < 2:
            u_obj.setEmpty()
            return u_obj
        
        enum_index = 1
        
        if obj_tuple[0] == Tokens.TYPEDEF:
            if len(obj_tuple) < 3:
                u_obj.setEmpty()
                return u_obj
            enum_index = 2
        
        u_obj.setEnum()
        u_obj.setTypedef()
        u_obj.setTypedefName(obj_tuple[enum_index])
        u_obj.setDataTypeStr(Tokens.INT32_T)
        
        #print("Found enum", u_obj.getTypedefName())
        
        return u_obj
        
if __name__ == '__main__':
    fParser = FileParser()
    #file_to_parse = "/home/maxr/Desktop/PYTHON_Workspace/LRADS_PPP_US/src/controllers/ThermalController.h"
    file_to_parse = "/home/maxr/Desktop/Work/lrads_ppp_us/src/tasks/logged_data_types.h"
    file_to_parse = "/home/maxr/Desktop/Work/lrads_ppp_us/src/tasks/config_io_task.h"
    
    obj_list = fParser.parseFile(file_to_parse)
    
    
    for o in obj_list:
        if o.getInstanceName() == "NUM_CELLS":
            print(o)
            
#        if o.getDataTypeStr() == "ioLoggedData":
#            print(o.getMemberVars())
    