# ExpressGui
ExpressGui is a gui for expressvpn on linux.

ExpressGui will simply call the commands of the command line expressvpn program and connect them to a gui.

Work in progress.

Building
--------
There are 2 build taget options.

One that uses cython to compile to an exe and the other is just a normal python script. Python script is default

Build as python script:

make

Build with cython:
```sh
make cython
```
Installation
------------
	sudo make install

Screenshots
-----------
![Screenshot](https://github.com/pancaketest/ExpressGui/raw/master/screenshots/window.png)

![Screenshot](https://github.com/pancaketest/ExpressGui/raw/master/screenshots/locationchooser.png)