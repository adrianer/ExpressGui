from setuptools import setup
from Cython.Build import cythonize


setup(name = 'express_gui',
      ext_modules = cythonize("*.py"))