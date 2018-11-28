from distutils.core import setup
from Cython.Build import cythonize
"""
Build command: python setup.py build_ext --inplace
"""

ext_options = {"annotate": True}

setup(name='calc', ext_modules=cythonize('calc.pyx', **ext_options), requires=['pandas', 'Cython', 'numpy', 'PyQt5'])
