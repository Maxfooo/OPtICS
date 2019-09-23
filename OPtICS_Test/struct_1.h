#ifndef STRUCT_1_H_
#define STRUCT_1_H_

struct STRUCT_0
{
	float pencil;
};


typedef struct 
{
	uint32_t reg[20];
	struct STRUCT_0 struct_0;
} __attribute__((packed)) STRUCT_1;


#endif// STRUCT_1_H_