CC ?= gcc-13
CFLAGS ?= -std=c11 -O1 -g -Wall -Wextra -Wpedantic -Werror
LDFLAGS ?= -pthread
ACTIVITIES := dsa-f-lab-01 dsa-f-lab-02 dsa-f-lab-03 dsa-f-lab-04 dsa-f-lab-05

.PHONY: all clean asan ubsan $(ACTIVITIES)
all: $(ACTIVITIES)

$(ACTIVITIES):
	@python3 -c "from pathlib import Path; Path('build').mkdir(exist_ok=True)"
	$(CC) $(CFLAGS) labs/$@/main.c -o build/$@ $(LDFLAGS)

asan: CFLAGS += -fsanitize=address -fno-omit-frame-pointer
asan: clean all

ubsan: CFLAGS += -fsanitize=undefined -fno-sanitize-recover=all
ubsan: clean all

clean:
	rm -rf build

