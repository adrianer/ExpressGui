BUILD_DIR=build
TARGET=expressgui
MAIN=expressgui.py
FILES=build/expressgui.c
EXPRESS_GUI=$(wildcard build/express_gui/*.c)
EXPRESSVPN=$(wildcard build/expressvpn/*.c)
FILEz=expressgui.o expressvpn.o location_picker.o parser.o window.o preferences.o server.o preferencer.o menu.o
INCLUDE=/usrinclude/python3.5m
LIBS=-lpython3.5m
CC=gcc
OPTS=-Os

python:
	cp -v expressgui.py expressgui
	chmod +x expressgui

cython:
	make -C express_gui cython
	make -C expressvpn cython
	mkdir -p cython
	cp -R -v express_gui/express_gui cython
	cp -R -v expressvpn/expressvpn cython
	cython --embed $(MAIN)
	$(CC) $(OPTS) -I /usr/include/python3.5m expressgui.c $(LIBS) -o expressgui
	cp -v expressgui cython/

clean:
	rm -f $(TARGET)
	rm -v -R -f $(BUILD_DIR)
	rm -v -f ./*.c
	make -C express_gui clean
	make -C expressvpn clean

