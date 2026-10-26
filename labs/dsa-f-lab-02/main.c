#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
typedef enum { BANK_FREE, BANK_FILLING, BANK_READY, BANK_PROCESSING } BankState;
static bool transition(BankState *state, BankState next) { (void)state; (void)next; return false; }
static uint32_t field_replace(uint32_t old, uint32_t mask, unsigned shift, uint32_t value) { (void)mask; (void)shift; (void)value; return old; }
int main(void) {
    BankState state = BANK_FREE;
    if (!transition(&state, BANK_FILLING) || field_replace(0xA5A50000u, 0x0000F000u, 12u, 3u) != 0xA5A53000u) {
        fputs("FAIL: implement ownership transitions and isolated field replacement\n", stderr); return 1;
    }
    puts("PASS: dsa-f-lab-02 public contract"); return 0;
}

