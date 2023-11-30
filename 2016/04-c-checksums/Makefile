# Some colors for @echo -e
FMT_DO=\e[0;33m
FMT_OK=\e[0;32m
FMT_ITEM=\e[1;34m
FMT_CLEAR=\e[0m

OS := $(shell uname -s)
SHELL := bash

CC := gcc
CFLAGS := -O3 -std=c11 -fstack-protector-all -Wstack-protector -Wall -Wextra -pedantic
DEBUG := -g3 -DDEBUG=1
LDFLAGS := -l pcre2-8
TEST_LIBS := -l cmocka -L /usr/lib

# Results
RUN_BIN := build/run
TEST_BIN := build/run-tests

# Objects
SOURCES := $(notdir $(basename $(wildcard src/*.c)))
OBJECTS := $(patsubst %,build/%.o,$(SOURCES))
TEST_OBJECTS := $(filter-out build/main.o,$(OBJECTS))


#
# Targets
#
default: build

# Link and build target
build: $(OBJECTS)
	@echo -en "$(FMT_DO)LD:$(FMT_CLEAR) ";
	$(CC) -o $(RUN_BIN) $+ $(DEBUG) $(CFLAGS) $(LDFLAGS)
	@echo -e "$(FMT_OK)OK:$(FMT_CLEAR) $(RUN_BIN)";

run-example: build
	@echo -e "$(FMT_DO)Run:$(FMT_CLEAR) $(RUN_BIN)";
	./$(RUN_BIN) example.txt

run: build
	@echo -e "$(FMT_DO)Run:$(FMT_CLEAR) $(RUN_BIN)";
	./$(RUN_BIN) input.txt

build/%.o: src/%.c
	mkdir -p build
	@echo -en "$(FMT_DO)CC:$(FMT_CLEAR) ";
	$(CC) -c $^ -o $@ $(DEBUG) $(CFLAGS)  # $(LDFLAGS)
	@echo -e "$(FMT_OK)OK:$(FMT_CLEAR) $@";

run-valgrind: build
	valgrind \
		--track-origins=yes \
		--leak-check=full \
		--leak-resolution=high \
		--log-file=valgrind.txt \
		./$(RUN_BIN) input.txt
	@echo -e "$(FMT_ITEM)Log:$(FMT_CLEAR) valgrind.txt"

build-tests: $(TEST_OBJECTS)
	@echo "$(TEST_OBJECTS)";
	@echo -en "$(FMT_DO)CC:$(FMT_CLEAR) ";
	$(CC) tests/main.c -o $(TEST_BIN) $+ $(DEBUG) $(CFLAGS) $(LDFLAGS) $(TEST_LIBS)
	@echo -e "$(FMT_OK)OK:$(FMT_CLEAR) $(TEST_BIN)";

# Compile and run tests
run-tests: build-tests
	@echo -e "$(FMT_DO)Run tests:$(FMT_CLEAR) $(TEST_BIN)"
	./$(TEST_BIN)

# Rule for cleaning the project
clean:
	@rm -vf build/* valgrind*.txt


.PHONY: default build run-example run run-valgrind build-tests run-tests clean build-dir
