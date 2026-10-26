#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

enum { RING_SIZE = 8 };
typedef struct { uint8_t data[RING_SIZE]; unsigned head, tail, dropped; } Ring;

static bool push(Ring *ring, uint8_t value) {
    (void)ring; (void)value;
    /* TODO: reserve one slot, reject and count a full write. */
    return false;
}
static bool pop(Ring *ring, uint8_t *value) {
    (void)ring; (void)value;
    /* TODO: return the next accepted value without shifting storage. */
    return false;
}
int main(void) {
    Ring ring = {0}; uint8_t value = 0;
    if (!push(&ring, 1) || !pop(&ring, &value) || value != 1) {
        fputs("FAIL: implement bounded ring invariants\n", stderr); return 1;
    }
    puts("PASS: dsa-f-lab-01 public contract"); return 0;
}

