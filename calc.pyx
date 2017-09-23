#include <iostream>

cpdef void fib(unsigned long long int n):
    cdef unsigned long long int a=0
    cdef unsigned long long int b=1
    while b < n:
        a, b = b, a + b
        print(b)
