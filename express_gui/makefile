CYTHON=cython

cython:
	mkdir -p express_gui
	python setup.py build_ext --inplace
	
clean:
	rm -v -R -f $(BUILD_DIR)
	rm -v -f ./*.c
	rm -v -f -R express_gui