# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:06:09 2019

@author: MaxR
"""

import CppObject
import Tokens
import Utils

print_found_objects = False

class FileParser(object):
    def __init__(self):
        self.obj_list = list()
        self.code_reg = Tokens.CodeRegex()
        self.current_file_name = ""
        self.current_line_num = 0
        
    def parseFileList(self, fileList):
        for f in fileList:
            
            self.obj_list.append(self.parseFile(f))
        return self.obj_list
    
    def parseFile(self, file):
        
        self.current_file_name = file
        
        print(file)
        
        obj_list = list()
        
        making_struct = False
        s_obj_q = list()
        s_obj_q_index = 0
        
        block_comment = False
        comment_index = -1
        block_comment_index = -1
        
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
                    continue
                
                ################################
                # Check for commented out code #
                ################################
                comment_index = line.find("//")
                if (comment_index > -1):
                    block_comment_index = line.find("/*")
                    if block_comment_index > -1:
                        if comment_index < block_comment_index:
                            # // /*  - will comment out the block comment
                            continue
                        else:
                            # /* //  - will block comment out the comment
                            block_comment = True
                            continue
                        
                    if "*/" in line:
                        # regular '//' comment does not affect the terminating block comment
                        block_comment = False
                        continue
                            
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
                # 2) Preprocessor keywords       #
                # 3) Variables                   #
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
#                    else:
#                        obj_list.append(cpp_obj)
#                        if print_found_objects:
#                            print("Found array")
#                            print(match_list)
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
            
    def startStructObj(self, structMatchList):
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
    
    def finishStructObj(self, structMatchList, s_obj):
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
        
    def makeDefineObj(self, matchList):
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
    
    def makeConstexprObj(self, matchList):
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
    
    def makeTypedefObj(self, matchList):
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
    
    def makeArrayObj(self, matchList):
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
        
    
    def makeVarObj(self, matchList):
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
        
        if u_obj.getInstanceName() == "scan_dir":
            print("Found scan_dir variable")
            print("scan_dir data type: ", u_obj.getDataTypeStr())
        
        return u_obj
        
        
    def makeEnumObj(self, matchList):
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
    fParser.parseFile("/home/maxr/Desktop/PYTHON_Workspace/LRADS_PPP_US/src/controllers/ThermalController.h")
    print("Ran FileParser.py")
    
    