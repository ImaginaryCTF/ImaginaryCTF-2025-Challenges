## Overview
Main idea is the same as the Fiesty Cipher challenge that we had in the May monthly, that is if the keys are palindromic, ie 
```math
\text{key}_0 = \text{key}_n
```
```math
\text{key}_1 = \text{key}_{n-1}
```
```math
\text{...}
```
```math
\text{key}_{n/2} = \text{key}_{n/2 + 1}
```
Then the encryption process of a Feistel Cipher is (almost) identical to the decryption process. So all we have to do is find a seed that results in a palindromic sequence of length 623. Constant value states are even simpler so we'll be trying to find one of those.

## The Actual Challenge
Unfortionately we need to look at cpythons _randommodule.c for this, (I'm so sorry Crypto bros). The two functions we care about are the init_by_array function and the genrand_uint32 function. Looking at init_by_array, we see that only states that begin with 0x80000000 are possible to seed, but other than that we can easily find a seed to achieve any state. The genrand_uint32 function really consists of 2 parts which randcrack calls "harden", and "regen", of which only regen will be relevant. The Regen portion is entered every 624 times genrand_uint32 is called and during the first call
~~~
for (kk=0;kk<N-M;kk++) {  
    y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);  
    mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1U];  
}
for (;kk<N-1;kk++) {  
    y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);  
    mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1U];  
}  
y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);  
mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1U];  
~~~
where mt is the state vector for the mersenne twister (a vector of 624 32 bit integers)  
This is quite nonlinear but sequences of 623 are actually easy to find if they're in the form  
```math
\text{mt}_0 = \text{A}
```
```math
\text{mt}_1 = \text{B}
```
```math
\text{...}
```
```math
\text{mt}_{226} = \text{B}
```
```math
\text{mt}_{227} = \text{0}
```
```math
\text{...}
```
```math
\text{mt}_{623} = \text{0}
```

so we can just brute force a value of $B$ with $A =$ 0x80000000
~~~
uint32_t val = 0;
    for (; val < 0xFFFFFFFE; ++val) {
        uint32_t mt[3] = { 0x80000000,val,val };
        int kk = 0;
        uint32_t y;
        static const uint32_t mag01[2] = { 0x0U, MATRIX_A };

        for (kk = 0; kk < 2; kk++) {
            y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK);
            mt[kk] = 0 ^ (y >> 1) ^ mag01[y & 0x1U];
        }
        if (mt[0] == mt[1]) {
            break;
        }
    }
    uint32_t mt[624];
    for (int i = 0; i < 624; ++i) {
        if (i < 227) {
            mt[i] = val;
        }
        else {
            mt[i] = 0;
        }
    }
~~~

Convert the array to a seed and its the same as the monthly challenge. Grab the encrypted flag split into 2 32 byte chunks, reverse the order of the two and ask the server to encrypt the recombined chunks. Reverse the order of the chunks again and that's the flag.

There (probably) isn't a seedable constant value sequence of length > 623 , but there might a general palindromic one, if anyone managed to find one we'd love to hear how you did it :)
