#ifndef STRUCT_2_H_
#define STRUCT_2_H_

#include "../struct_1.h"

typedef uint8_t my_int_t;
constexpr my_int_t MY_SIZE = 100; 

struct STRUCT_2 {
	bool ok;
	my_int_t my_arr[MY_SIZE];
};


#endif // STRUCT_2_H_