from setuptools import setup
from Cython.Build import cythonize

setup(name = 'expressvpn',
      ext_modules = cythonize("*.py"))