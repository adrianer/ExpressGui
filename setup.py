from setuptools import setup
from Cython.Build import cythonize
import sys



#setup(name = 'expressvpn',
		#packages = ['expressvpn','express_gui'])
#setup(name = 'expressvpn',
	 #ext_modules = cythonize("expressvpn/*.py"))
#if "cython" not in sys.argv:
#	setup(name = 'expressvpn',
#		packages = ['expressvpn','express_gui'])
#else:
if "build_ext" in sys.argv:
	setup(name="test",
		ext_modules = cythonize("expressvpn/*.py"))
	setup(name="test",
		ext_modules = cythonize("express_gui/*.py"))
elif "build" in sys.argv:
	setup(packages=["expressvpn","express_gui"])
else:
	setup()