# ExpressGui
ExpressGui is a gui for expressvpn on linux.

ExpressGui will simply call the commands of the command line expressvpn program and connect them to a gui.

Work in progress.

Building
--------
There are 2 build taget options.

One that uses cython to compile to an exe and the other is just a normal python script. Cython isn't needed of course I just wanted to try cython out and i've left it here because why not. Python script is the default make target.

Build as python script:
```shell
make
```

Build with cython:
```shell
make cython
```
Installation
------------
	sudo make install

Screenshots
-----------
![Screenshot](https://github.com/pancaketest/ExpressGui/raw/master/screenshots/window.png)

![Screenshot](https://github.com/pancaketest/ExpressGui/raw/master/screenshots/locationchooser.png)