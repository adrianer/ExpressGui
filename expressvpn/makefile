BUILD_DIR=build

exe:
	mkdir -p $(BUILD_DIR)
	make $(DEPS) -B

cython:
	mkdir -p expressvpn
	python setup.py build_ext --inplace

clean:
	rm -v -R -f $(BUILD_DIR)
	rm -v -f ./*.c
	rm -v -f -R expressvpn