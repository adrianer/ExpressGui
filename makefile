BUILD_DIR=build
TARGET=expressgui
MAIN=expressgui.py
FILES=build/expressgui.c
EXPRESS_GUI=$(wildcard build/express_gui/*.c)
EXPRESSVPN=$(wildcard build/expressvpn/*.c)
INCLUDE=/usrinclude/python3.5m
LIBS=-lpython3.5m
CC=gcc
OPTS=-Os

python:
	cp -v expressgui.py expressgui
	chmod +x expressgui

exe:
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_DIR)/express_gui
	mkdir -p $(BUILD_DIR)/expressvpn
	make -C express_gui exe
	cp -v express_gui/build/* $(BUILD_DIR)/express_gui
	make -C expressvpn exe
	cp -v expressvpn/build/* $(BUILD_DIR)/expressvpn
	cython --embed $(MAIN) -o build/
	make compile

compile:
	$(CC) $(OPTS) -I /usr/include/python3.5m $(FILES) $(EXPRESS_GUI) $(EXPRESSVPN) $(LIBS) -o $(TARGET)


clean:
	rm -f $(TARGET)
	rm -v -R -f $(BUILD_DIR)
	make -C express_gui clean
	make -C expressvpn clean

