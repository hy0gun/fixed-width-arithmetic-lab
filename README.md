# Fixed-Width Arithmetic Lab

Run bits.py in PyCharm. Input widths 2-16; decimal values, 0b binary, or 0x hex. Nonnegative inputs are unsigned bit patterns. Negative inputs are signed integers and must fit the signed range. Enter q at the width prompt to exit.

## Features
Binary/hex/signed/unsigned interpretations, checked signed encoding, wrapped addition, independent overflow checks, textual derivations, and a visual HTML explanation of the exact calculation. After entering two operands, open calculation.html beside the code.

## Walkthrough
parse chooses base from a prefix. decode validates the width and pattern, then subtracts 2**width if the sign bit is one. encode_signed checks signed bounds and wraps a negative integer into its bit pattern. addition uses modulo for wrapping and checks signed and unsigned mathematical sums separately. explain generates the derivation; report creates an offline HTML bit table and explanation.

Example: width 4, 7+1 -> 1000, unsigned 8, signed -8. Signed sum 8 exceeds maximum 7: signed overflow only. Width 4, -1+1 encodes patterns 1111+0001 -> 0000; signed sum 0 fits, unsigned pattern sum 16 exceeds 15: unsigned overflow only.

## Limits
A fixed-width arithmetic teaching tool, not a full CPU emulator. No subtraction/bitwise operations yet. Python integers are arbitrary-precision, so wrapping is explicitly simulated. Report bit weights are unsigned; the leading weight would be negative in signed interpretation.

## Your contributions
Generated implementation. Record your own changes and verification here.
