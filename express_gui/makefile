CYTHON=cython
DEPS=window.py location_picker.py menu.py preferences.py
BUILD_DIR=build
FILES=$(wildcard build/*.c)

exe:
	mkdir -p $(BUILD_DIR)
	make -B $(DEPS)

$(DEPS):
	$(CYTHON) $@ -o $(BUILD_DIR)
	
clean:
	rm -v -R -f $(BUILD_DIR)