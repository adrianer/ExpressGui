CYTHON=cython
CC=gcc
OPTS=-Os
DEPS=window.py location_picker.py
MAIN=app.py
BUILD_DIR=build
FILES=$(wildcard build/*.c)
EXPRESS=$(wildcard build/expressvpn/*.c)
INCLUDE=/usrinclude/python3.5m
LIBS=-lpython3.5m
TARGET=expressgui

exe:
	mkdir -p $(BUILD_DIR)
	cython --embed $(MAIN) -o $(BUILD_DIR)
	make $(DEPS) -B
	make -C expressvpn
	mkdir -p $(BUILD_DIR)/expressvpn
	cp -v expressvpn/build/* $(BUILD_DIR)
	$(MAKE) compile

$(DEPS):
	$(CYTHON) $@ -o $(BUILD_DIR)

compile:
	$(CC) $(OPTS) -I /usr/include/python3.5m -o $(TARGET) $(FILES) $(EXPRESS) $(LIBS)
	
clean:
	rm -R -f $(BUILD_DIR)
	rm -f $(TARGET)
	cd expressvpn && make clean