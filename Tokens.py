# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:06:44 2019

@author: MaxR
"""

import re
from Utils import regexFindall

# Using tuples to force write protection

DEFINE    = '#define'
CONSTEXPR = 'constexpr'
TYPEDEF   = 'typedef'
PreProcessor = tuple([DEFINE, CONSTEXPR, TYPEDEF])

CONST    = 'const'
VOLATILE = 'volatile'
MUTABLE  = 'mutable'
STATIC   = 'static'
Qualifiers = tuple([CONST, VOLATILE, MUTABLE, STATIC])


Avoid = tuple(['void', '\(\s*\)'])

UINT8_T  = 'uint8_t'
UINT16_T = 'uint16_t'
UINT32_T = 'uint32_t'
UINT64_T = 'uint64_t'
INT8_T   = 'int8_t'
INT16_T  = 'int16_t'
INT32_T  = 'int32_t'
INT64_T  = 'int64_t'
UNSIGNED_SHORT     = 'unsigned short'
UNSIGNED_SHORT_INT = 'unsigned short int'
SHORT     = 'short'
SHORT_INT = 'short int'
UNSIGNED_INT  = 'unsigned int'
UNSIGNED_LONG = 'unsigned long'
UNSIGNED_LONG_INT  = 'unsigned long int'
UNSIGNED_LONG_LONG = 'unsigned long long'
UNSIGNED_LONG_LONG_INT = 'unsigned long long int'
INT  = 'int'
LONG = 'long'
LONG_INT  = 'long int'
LONG_LONG = 'long long'
LONG_LONG_INT = 'long long int'
UNSIGNED_CHAR = 'unsigned char'
CHAR    = 'char'
WCHAR_T = 'wchar_t'
FLOAT   = 'float'
DOUBLE  = 'double'
LONG_DOUBLE = 'long double'
BOOL   = 'bool'
STRING = 'string'
STD_STRING = 'std::string'

DataTypes = tuple([ UINT8_T,  \
                    UINT16_T, \
                    UINT32_T, \
                    UINT64_T, \
                    INT8_T,   \
                    INT16_T,  \
                    INT32_T,  \
                    INT64_T,  \
                    UNSIGNED_SHORT,     \
                    UNSIGNED_SHORT_INT, \
                    SHORT,     \
                    SHORT_INT, \
                    UNSIGNED_INT,  \
                    UNSIGNED_LONG, \
                    UNSIGNED_LONG_INT,  \
                    UNSIGNED_LONG_LONG, \
                    UNSIGNED_LONG_LONG_INT, \
                    INT,  \
                    LONG, \
                    LONG_INT,  \
                    LONG_LONG, \
                    LONG_LONG_INT, \
                    UNSIGNED_CHAR, \
                    CHAR,    \
                    WCHAR_T, \
                    FLOAT,   \
                    DOUBLE,  \
                    LONG_DOUBLE, \
                    BOOL])

NpTypeMap = {UINT8_T : 'np.uint8',  \
            UINT16_T : 'np.uint16', \
            UINT32_T : 'np.uint32', \
            UINT64_T : 'np.uint64', \
            INT8_T   : 'np.int8',   \
            INT16_T  : 'np.int16',  \
            INT32_T  : 'np.int32',  \
            INT64_T  : 'np.int64',  \
            UNSIGNED_SHORT     : 'np.uint16', \
            UNSIGNED_SHORT_INT : 'np.uint16', \
            SHORT     : 'np.int16', \
            SHORT_INT : 'np.int16', \
            UNSIGNED_INT  : 'np.uint32', \
            UNSIGNED_LONG : 'np.uint32', \
            UNSIGNED_LONG_INT  : 'np.uint32', \
            UNSIGNED_LONG_LONG : 'np.uint64', \
            UNSIGNED_LONG_LONG_INT : 'np.uint64', \
            INT  : 'np.int32', \
            LONG : 'np.int32', \
            LONG_INT  : 'np.int32', \
            LONG_LONG : 'np.int64', \
            LONG_LONG_INT : 'np.int64', \
            UNSIGNED_CHAR : 'np.uint8', \
            CHAR    : 'np.int8',    \
            WCHAR_T : 'np.int16',   \
            FLOAT   : 'np.float32', \
            DOUBLE  : 'np.float64', \
            LONG_DOUBLE : 'np.float64', \
            BOOL   : 'np.uint8', \
            STRING : 'np.int8',  \
            STD_STRING  : 'np.int8' }

class CodeRegex(object):
    def __init__(self):
        self.data_types_tokens = "("        
        for d in DataTypes:
            self.data_types_tokens += "("
            self.data_types_tokens += "{}".format(d)
            self.data_types_tokens += ")*"
        self.data_types_tokens += "(\w+)*" # catch generic names
        self.data_types_tokens += ")"
            
        self.qualifiers_tokens = "("
        for q in Qualifiers:
            self.qualifiers_tokens += "("
            self.qualifiers_tokens += "{}".format(q)
            self.qualifiers_tokens += ")*"
        self.qualifiers_tokens += ")"
            
        self.avoid_tokens = "("
        for a in Avoid:
            self.avoid_tokens += "("
            self.avoid_tokens += "{}".format(a)
            self.avoid_tokens += ")*"
        self.avoid_tokens += ")"
            
        #
        # AVOID REGEX
        #
        self.avoid_regex = "(\w+\s+\w+\([\w\s&+-/\*]*\))*" # catch functions
        self.avoid_regex += "{}".format(self.avoid_tokens)
        
        #
        # DEFINE REGEX
        #
        self.define_regex = "({})\s+(\w+)\s+(\w+)".format(DEFINE)
        
        #
        # CONSTEXPR REGEX
        #
        self.constexpr_regex = "({0})\s+{1}\s+(\w+)\s+=\s*(\w+);".format(CONSTEXPR, self.data_types_tokens)
        
        #
        # TYPEDEF REGEX
        #
        self.typedef_regex = "({0})\s+({1})\s+(\w+)\[*([\w+]*)\]*;".format(TYPEDEF, self.data_types_tokens)
        
        #
        # VARIABLE REGEX
        #
        self.variable_regex = "{0}\s*([{1}]+)\s+(\w+)\s*=*\s*([\w]*);".format(self.qualifiers_tokens, self.data_types_tokens)
        
        #
        # ARRAY REGEX
        #
        self.array_regex = "{0}\s*([{1}]+)\s+(\w+)(\[([\w]*)\])\s*".format(self.qualifiers_tokens, self.data_types_tokens)
        self.array_regex += "=*\s*\{*([\w\s,]*)\}*;"
        
        #
        # 2D ARRAY REGEX
        #
        # does NOT work at the moment
        self.array_2d_regex = "{0}\s*({1})\s+(\w+)(\[([\w+]*)\])\s*".format(self.qualifiers_tokens, self.data_types_tokens)
        self.array_2d_regex += "=*\s*\{*([\w\s,]*)\}*;"
        
        #
        # STRUCT HEAD REGEX
        #
        self.struct_head_regex = "({0})*\s*(struct)\s+(\w*)\s*(\w*)\[*([\w+]*)\]*(;*)".format(TYPEDEF)
        self.struct_head_regex += "\{*\s*"
        
        #
        # STRUCT TAIL REGEX
        #
        self.struct_tail_regex = "(\})([\s\w\(]*)\)*\s*(\w*);"
        
        #
        # STRUCT REGEX
        #
        self.struct_regex = self.getStructHeadRegex()
        self.struct_regex += "([\s\w;\[\]]*)" # body of struct
        self.struct_regex += self.getStructTailRegex()
        
            
    def getAvoidRegex(self):
        return self.avoid_regex
    
    def getDefineRegex(self):
        return self.define_regex
    
    def getConstexprRegex(self):
        return self.constexpr_regex
    
    def getTypedefRegex(self):
        return self.typedef_regex
    
    def getVariableRegex(self):
        return self.variable_regex
    
    def getArrayRegex(self):
        return self.array_regex
    
    def get2dArrayRegex(self):
        return self.array_2d_regex
    
    def getStructHeadRegex(self):
        return self.struct_head_regex
        
    def getStructTailRegex(self):
        return self.struct_tail_regex
    
    def getStructRegex(self):
        return self.struct_regex
    

if __name__ == '__main__':
    code_reg = CodeRegex()
    
    all_string = """ // all string
                    volatile uint8_t buffer = 0;
                    #define TEST_DEFINE 1
                    constexpr long double TEST_1_LONG_DOUBLE = 1;
                    typedef bool my_bool;
                    typedef char my_str[60];
                    typedef float my_floats[MY_FLOAT_SIZE];
                    long long my_array[20];
                    short my_array[] = {1, 2, 3, 4};
                    volatile int16_t my_array[ARRAY_SIZE+3];
                    typedef struct
                    {
                        uint32_t reg;
                        float max;
                    } __attribute__((packed)) MY_REG_T;
                    struct MY_REG_T {
                        uint32_t reg;
                        float max;
                        double list[20];
                    };
                    """
    print(all_string)
    
    all_string_list = [x.strip() for x in all_string.split("\n")]
    print(all_string_list)
    
    print("\n-----Test 'avoid' parsing-----")
    print(code_reg.getAvoidRegex())
    avoid_string = "void function_prototype();"
    avoid_string_2 = "int i = 0;"
    avoid_string_3 = "uint8_t function_proto(MY_CLASS* boop, const float& f); void"
    match_list = regexFindall(code_reg.getAvoidRegex(), avoid_string_3)
    print(match_list)
    
    
    print("\n-----Test variable parsing-----")
    var_string = "volatile uint8_t buffer = 0;"
    gen_var_string = "const MY_TYPE vari = 7;"
    var_string_2 = "std::string my_string;"
    print(code_reg.getVariableRegex())
    match_list = regexFindall(code_reg.getVariableRegex(), var_string_2)
    print(match_list)
    
    print("\n-----Test uninitialized variable parsing-----")
    var_string = "const unsigned short my_var;"
    match_list = regexFindall(code_reg.getVariableRegex(), var_string)
    print(match_list)    
    
    print("\n-----Test #define parsing-----")
    define_string = "#define TEST_DEFINE 1"
    print(code_reg.getDefineRegex())
    match_list = regexFindall(code_reg.getDefineRegex(), define_string)
    print(match_list)
    
    print("\n-----Test constexpr parsing-----")
    constexpr_string = "constexpr long double TEST_1_LONG_DOUBLE = 1;"
    constexpr_string_2 = "constexpr MY_TYPE_T MY_SIZE = 200;"
    print(code_reg.getConstexprRegex())
    match_list = regexFindall(code_reg.getConstexprRegex(), constexpr_string_2)
    print(match_list)
    
    print("\n-----Test typedef parsing-----")
    typedef_string = "typedef bool my_bool;"
    typedef_string_2 = "typedef my_bool my_other_bool;"
    print(code_reg.getTypedefRegex())
    match_list = regexFindall(code_reg.getTypedefRegex(), typedef_string_2)
    print(match_list)
    
    print("\n-----Test typedef array parsing-----")
    typedef_string = "typedef char my_str[60];"
    match_list = regexFindall(code_reg.getTypedefRegex(), typedef_string)
    print(match_list)
    
    print("\n-----Test typedef array with typedef size-----")
    typedef_string = "typedef float my_floats[MY_FLOAT_SIZE];"
    match_list = regexFindall(code_reg.getTypedefRegex(), typedef_string)
    print(match_list)
    
    print("\n-----Test array parsing-----")
    array_string = "unsigned long long my_array[20];"
    array_string_2 = " arr[n] = 0;"
    print(code_reg.getArrayRegex())
    match_list = regexFindall(code_reg.getArrayRegex(), array_string_2)
    print(match_list)    
    
    print("\n-----Test initialized array parsing-----")
    array_string = "short my_array[] = {1, 2, 3, 4};"
    match_list = regexFindall(code_reg.getArrayRegex(), array_string)
    print(match_list)
    
    print("\n-----Test array with typedef size-----")
    array_string = "volatile int16_t my_array[ARRAY_SIZE];"
    match_list = regexFindall(code_reg.getArrayRegex(), array_string)
    print(match_list)
    
    print("\n-----Test 2D array parsing-----")
    array_string = "bool field[ROW][10];"
    match_list = regexFindall(code_reg.get2dArrayRegex(), array_string)
    print(match_list)
    
    print("\n-----Test struct string parsing-----")
    struct_string = """
                    typedef struct
                    {
                        uint32_t reg;
                        float max;
                    } __attribute__((packed)) MY_REG_T;
                    """
    
    print(code_reg.getStructRegex())
    match_list = regexFindall(code_reg.getStructRegex(), struct_string)
    print(match_list)
    
    print("\n-----Test struct string 2 parsing-----")
    struct_string_2 = """
                      struct MY_REG_T {
                          uint32_t reg;
                          float max;
                          double list[20];
                      };
                      """
    struct_string_3 = """
                      struct MY_STRUCT_HEADER {
                      """
    struct_string_4 = """
                      #include "../struct_1.h"
                      """
    struct_string_5 = "struct MyStruct my_struct;"
    struct_string_6 = "MY_STRUCT my_struct;" #too generic
    
    
    match_list = regexFindall(code_reg.getStructRegex(), struct_string_6)
    print(match_list)
    
    print("\n-----Test struct head parsing-----")
    print(code_reg.getStructHeadRegex())
    struct_string_2 = """
                    struct YOUR_STRUCT your_struct;
                    """
    match_list = regexFindall(code_reg.getStructHeadRegex(), struct_string)
    print(match_list)
    
    print("\n-----Test struct tail parsing-----")
    struct_string_2 = """
                    typedef struct
                    {
                      bool   enabled;
                      float setpoint;
                      float feedback;
                      float correction;
                    } __attribute__((__packed__)) cc_log_t;
                    """
    print(code_reg.getStructTailRegex())
    match_list = regexFindall(code_reg.getStructTailRegex(), struct_string_2)
    print(match_list)
    
    print("\n-----Test complete string parsing-----")
    match_list = regexFindall(code_reg.getStructRegex(), all_string)
    print(match_list)
    
    
    
    
    
    
    
    
    
    
    
    