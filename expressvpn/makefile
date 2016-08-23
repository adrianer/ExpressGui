CYTHON=cython
CC=gcc
INCLUDE=
DEPS=expressvpn.py preferences.py server.py parser.py
BUILD=build
FILES=$(wildcard *.c)

cython:
	mkdir -p build
	make $(DEPS) -B

$(DEPS):
	$(CYTHON) $@ -o build

clean:
	rm -R -f build