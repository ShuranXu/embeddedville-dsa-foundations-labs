#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
typedef enum { WAIT_SYNC, READ_LENGTH, READ_PAYLOAD, READ_CHECK } ParseState;
typedef struct { ParseState state; uint8_t payload[16]; size_t length, index; unsigned frames, errors; } Parser;
static void feed(Parser *parser, uint8_t byte) { (void)parser; (void)byte; }
int main(void) {
    Parser parser = {0}; const uint8_t frame[] = {0xAAu, 1u, 0x2Au, 0x2Au};
    for (size_t i = 0; i < sizeof frame; ++i) feed(&parser, frame[i]);
    if (parser.frames != 1u) { fputs("FAIL: implement bounded streaming parser states\n", stderr); return 1; }
    puts("PASS: dsa-f-lab-05 public contract"); return 0;
}
