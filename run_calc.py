import calc
import timeit
import numpy as np
import pandas as pd
"""
max unsigned long long int = 18446744073709551615
"""

# calc.fib(99)
print('\nspent time {}'.format(timeit.timeit('calc.fib(9999999999999999999)', number=1, globals=globals())))

# a = np.zeros(100, np.int64)
