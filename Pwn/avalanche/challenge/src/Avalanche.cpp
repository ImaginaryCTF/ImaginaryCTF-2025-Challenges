/*
 * Avalanche.cpp
 *
 *  Created on: May 19, 2025
 *      Author: moaiman
 *	
 *	This cannot be compiled with gcc, and should be compiled with clang for the intended behavior 
 */
#include <stdint.h>
#include <iostream>
#include <stdio.h>
#include <cstdlib>
#include <cstring>

uint64_t occupancy = 0;

constexpr size_t bufferSize = 31;


char flag[128] = { 0 };
const char* choice_message = "\npress 1 to print the flag, press 2 to leave a number)\t";
const char* intro = "sorry some l33t h4ck3r broke our flag printer, if you like you may leave your phone number and we'll get back to you when we've fixed it";
const char* number_prompt = "\nEnter your phone number and we'll add it to our database\t";
const char* reserved_message = "\nsorry that number is reserved\n";
const char* flag_message = "\nsure heres the flag ";

const char* error_message = "\n\ndon't try and break me >:V";
const char* bozo = "QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ\nQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ\nQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ\nQQQQQQQQQQQQQQQQQQQWQQQQQWWWBBBHHHHHHHHHBWWWQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ\nQQQQQQQQQQQQQQQD!`__ssaaaaaaaaaass_ass_s____.  -~\"\"??9VWQQQQQQQQQQQQQQQQQQQ\nQQQQQQQQQQQQQP'_wmQQQWWBWV?GwwwmmWQmwwwwwgmZUVVHAqwaaaac,\"?9$QQQQQQQQQQQQQQ\nQQQQQQQQQQQW! aQWQQQQW?qw#TTSgwawwggywawwpY?T?TYTYTXmwwgZ$ma/-?4QQQQQQQQQQQ\nQQQQQQQQQQW' jQQQQWTqwDYauT9mmwwawww?WWWWQQQQQ@TT?TVTT9HQQQQQQw,-4QQQQQQQQQ\nQQQQQQQQQQ[ jQQQQQyWVw2$wWWQQQWWQWWWW7WQQQQQQQQPWWQQQWQQw7WQQQWWc)WWQQQQQQQ\nQQQQQQQQQf jQQQQQWWmWmmQWU???????9WWQmWQQQQQQQWjWQQQQQQQWQmQQQQWL 4QQQQQQQQ\nQQQQQQQP'.yQQQQQQQQQQQP\"       <wa,.!4WQQQQQQQWdWP??!\"??4WWQQQWQQc ?QWQQQQQ\nQQQQQP'_a.<aamQQQW!<yF \"!` ..  \"??$Qa \"WQQQWTVP'    \"??' =QQmWWV?46/ ?QQQQQ\nQQQP'sdyWQP?!`.-\"?46mQQQQQQT!mQQgaa. <wWQQWQaa _aawmWWQQQQQQQQQWP4a7g -WWQQ\nQQ[ j@mQP'adQQP4ga, -????\" <jQQQQQWQQQQQQQQQWW;)WQWWWW9QQP?\"`  -?QzQ7L ]QQQ\nQW jQkQ@ jWQQD'-?$QQQQQQQQQQQQQQQQQWWQWQQQWQQQc \"4QQQQa   .QP4QQQQfWkl jQQQ\nQE ]QkQk $D?`  waa \"?9WWQQQP??T?47`_aamQQQQQQWWQw,-?QWWQQQQQ`\"QQQD\\Qf(.QWQQ\nQQ,-Qm4Q/-QmQ6 \"WWQma/  \"??QQQQQQL 4W\"- -?$QQQQWP`s,awT$QQQ@  \"QW@?$:.yQQQQ\nQQm/-4wTQgQWQQ,  ?4WWk 4waac -???$waQQQQQQQQF??'<mWWWWWQW?^  ` ]6QQ' yQQQQQ\nQQQQw,-?QmWQQQQw  a,    ?QWWQQQw _.  \"????9VWaamQWV???\"  a j/  ]QQf jQQQQQQ\nQQQQQQw,\"4QQQQQQm,-$Qa     ???4F jQQQQQwc <aaas _aaaaa 4QW ]E  )WQ`=QQQQQQQ\nQQQQQQWQ/ $QQQQQQQa ?H ]Wwa,     ???9WWWh dQWWW,=QWWU?  ?!     )WQ ]QQQQQQQ\nQQQQQQQQQc-QWQQQQQW6,  QWQWQQQk <c                             jWQ ]QQQQQQQ\nQQQQQQQQQQ,\"$WQQWQQQQg,.\"?QQQQ'.mQQQmaa,.,                . .; QWQ.]QQQQQQQ\nQQQQQQQQQWQa ?$WQQWQQQQQa,.\"?( mQQQQQQW[:QQQQm[ ammF jy! j( } jQQQ(:QQQQQQQ\nQQQQQQQQQQWWma \"9gw?9gdB?QQwa, -??T$WQQ;:QQQWQ ]WWD _Qf +?! _jQQQWf QQQQQQQ\nQQQQQQQQQQQQQQQws \"Tqau?9maZ?WQmaas,,    --~-- ---  . _ssawmQQQQQQk 3QQQQWQ\nQQQQQQQQQQQQQQQQWQga,-?9mwad?1wdT9WQQQQQWVVTTYY?YTVWQQQQWWD5mQQPQQQ ]QQQQQQ\nQQQQQQQWQQQQQQQQQQQWQQwa,-??$QwadV}<wBHHVHWWBHHUWWBVTTTV5awBQQD6QQQ ]QQQQQQ\nQQQQQQQQQQQQQQQQQQQQQQWWQQga,-\"9$WQQmmwwmBUUHTTVWBWQQQQWVT?96aQWQQQ ]QQQQQQ\nQQQQQQQQQQWQQQQWQQQQQQQQQQQWQQma,-?9$QQWWQQQQQQQWmQmmmmmQWQQQQWQQW(.yQQQQQW\nQQQQQQQQQQQQQWQQQQQQWQQQQQQQQQQQQQga%,.  -??9$QQQQQQQQQQQWQQWQQV? sWQQQQQQQ\nQQQQQQQQQWQQQQQQQQQQQQQQWQQQQQQQQQQQWQQQQmywaa,;~^\"!???????!^`_saQWWQQQQQQQ\nQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQWWWWQQQQQmwywwwwwwmQQWQQQQQQQQQQQ\nQQQQQQQWQQQWQQQQQQWQQQWQQQQQWQQQQQQQQQQQQQQQQWQQQQQWQQQWWWQQQQQQQQQQQQQQQWQ\n\n";




uint64_t siphash24(const void* src, unsigned long src_sz, const char key[16]);




uint64_t hash(uint64_t a) {
	const unsigned char* casted = (const unsigned char*)(&a);
	char key[16] = { 'I','m','a','g','i','n','a','r','y','C','T','F','2','0','2','5' };
	return siphash24(casted,8,key);
}




void insert(const volatile uint64_t& value, volatile uint64_t* begin, volatile uint64_t* end) {
	size_t length = end - begin;
	uint64_t position = (hash(value) % length);
	while (true) {
		if (begin[position] == 0 || begin[position] == value) {
			occupancy += begin[position] == 0;
			begin[position] = value;
			
			return;
		}
		position += 1;
	}
	return;
}

bool stack_guard(volatile uint64_t* begin, size_t length) {
	for (int i = 0; i < length; ++i) {
		if (begin[i] != 0) {
			return false;
		}
	}
	return true;

}


/*
void readflag() {
	std::ifstream file("flag.txt", std::ios::binary);
	if (!file) { 
		std::cout << "the flag is missing please contact ictf admins" << std::endl;
		exit(1);
	}
	file.read(flag, 128);
	if (file.bad()) {
		std::cout << "something went very wrong please contact ictf admins" << std::endl;
		exit(1);
	}
}
*/

//I'm bad at k8 and can't figure out how to write the flag file dynamically so I guess we're using env variables now
void readflag() {
    const char* env_flag = std::getenv("FLAG");
    if (!env_flag) {
        std::cout << "the flag is missing please contact ictf admins" << std::endl;
        exit(1);
    }
    std::strncpy(flag, env_flag, 127);
    flag[127] = '\0';
}




void rehash(volatile uint64_t &l, volatile uint64_t& L, volatile uint64_t* &begin, volatile uint64_t* &array_begin) {
	if (l > 64) {
		std::cout << "sorry our server can't process that many numbers please come back later" << std::endl;
		exit(1);
	}
	occupancy = 0;

	uint64_t new_L = (3 * l + 2 - L);
	memset((char*)array_begin, 0, 8 * (L + new_L - l));


	memcpy((char*)array_begin, (char*)begin, 8 * l);
	memset((char*)begin, 0, 8 * l);
	begin = array_begin + l;

	for (int i = 0; i < l; ++i) {
		insert(array_begin[i], begin, begin + (2 * l + 2));
	}
	memset((char*)array_begin, 0, l * 8);
	l = 2 * l + 2;
	L += new_L;
}


int main() {
	readflag();
	uint64_t choice = 0;

	
	volatile uint64_t l = 8;
	volatile uint64_t L = l;
	volatile uint64_t* begin;
	volatile uint64_t* array_begin;
	volatile uint64_t buffer[bufferSize + 1] = { 0 };


	begin = (uint64_t*)alloca(l * 8);
	memset((char*)begin, 0, l * 8);


	std::cout << intro << std::endl;
	while (true) {
		choice = 0;
		std::cout << choice_message;
		std::cin >> choice;
		if (choice == 1) {
			std::cout << flag_message;
			printf((char*)(&buffer[bufferSize]), flag);
			printf("\n\n");

			std::cout << bozo << std::endl;
		}

		else if (choice == 2) {
			std::cout << number_prompt;
			std::cin >> choice;
			if (std::cin.fail()) {
				break;
			}
			if (choice == 0) {
				std::cout << reserved_message << std::endl;
				continue;
			}


			insert((volatile uint64_t&) choice, begin, begin + l);
			if (!stack_guard(buffer, bufferSize)) {
				break;
			}
			if (occupancy == l) {
				//reserve enough space for 2 * l + 2 elements (l + 2 more than previously reserved) and l extra for a copy buffer during rehash
				array_begin = (volatile uint64_t*)alloca(8 * (3 * l + 2 - L));
				rehash(l, L, begin, array_begin);
			}



		}

		else if (std::cin.fail()) {
			break;
		}


	}
	std::cout << error_message << std::endl;




}



