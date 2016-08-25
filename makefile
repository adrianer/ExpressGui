BUILD_DIR=build
TARGET=expressgui
MAIN=expressgui.py
FILES=build/expressgui.c
INCLUDE=/usrinclude/python3.5m
LIBS=-lpython3.5m
CC=gcc
OPTS=-Os
INSTALL_PATH=/usr/local/bin

python:
	cp -v expressgui.py expressgui
	chmod +x expressgui
	python setup.py build

install: $(TARGET)
	python setup.py install_lib
	install expressgui $(INSTALL_PATH)

cython:
	python setup.py build_ext -b build/lib
	cython --embed expressgui.py
	$(CC) $(OPTS) -I /usr/include/python3.5m expressgui.c $(LIBS) -o expressgui

clean:
	rm -f $(TARGET)
	rm -v -R -f $(BUILD_DIR)
	rm -v -f ./*.c
	rm -v -f expressvpn/*.c
	rm -v -f express_gui/*.c
