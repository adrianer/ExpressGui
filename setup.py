from setuptools import setup
from Cython.Build import cythonize
import sys


if "build_ext" in sys.argv:
    setup(name="test",
          ext_modules=cythonize("expressvpn/*.py"))
    setup(name="test",
          ext_modules=cythonize("express_gui/*.py"))
elif "build" in sys.argv:
    setup(packages=["expressvpn", "express_gui"])
else:
    setup()
