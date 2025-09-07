#include <stdint.h>
#include <iostream>
#include <vector>


uint64_t siphash24(const void* src, unsigned long src_sz, const char key[16]);




uint64_t hash(uint64_t a) {
	const unsigned char* casted = (const unsigned char*)(&a);
	char key[16] = { 'I','m','a','g','i','n','a','r','y','C','T','F','2','0','2','5' };
	return siphash24(casted,8,key);
}




int main() {
	std::vector<uint64_t> v;
	//prefix = %s\00
	uint64_t prefix = 0x007325;
	constexpr uint64_t step = 0x1000000;
	uint64_t i = prefix;
	while (v.size() < 38) {
		uint64_t test = hash(i);
		if ((test % 17784) == 15048) {
			v.push_back(i);
		}
		i += step;
	}
	for (auto& entry : v) {
		std::cout << entry << std::endl;
	
	
	}
}
