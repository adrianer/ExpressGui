CYTHON=cython
DEPS=expressvpn.py preferences.py server.py parser.py
BUILD_DIR=build
FILES=$(wildcard *.c)

exe:
    mkdir -p $(BUILD_DIR)
    make $(DEPS) -B

$(DEPS):
    $(CYTHON) $@ -o $(BUILD_DIR)

clean:
    rm -v -R -f $(BUILD_DIR)