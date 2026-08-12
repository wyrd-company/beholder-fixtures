"""Numeric literals and arithmetic edges (PY-CAN-SRC-006).

Covers large/base/separated integers, float infinities and NaNs,
complex values, negative floor and modulo, and exponent precedence.
"""

import math
import sys

# Base-prefixed integers
hex_literal = 0xFF
hex_upper = 0X1A2B
oct_literal = 0o777
bin_literal = 0b1010_1100
bin_upper = 0B1010

# Separated integers (underscores)
separated_decimal = 1_000_000
separated_hex = 0xFF_FF
separated_bin = 0b1010_1010
separated_oct = 0o1_234

# Large integers
large_int = 10**100
large_hex = 0xFFFFFFFFFFFFFFFF
# Integer string digit limit (Python 3.11+): 4300 digits default; stay well below
large_but_within_limit = int("9" * 1000)
integer_digit_limit = sys.get_int_max_str_digits()  # 4300 on this build

# Float infinities and NaNs
inf_positive = float("inf")
inf_negative = float("-inf")
inf_from_math = math.inf
nan_value = float("nan")
nan_from_math = math.nan
nan_not_equal_self = nan_value != nan_value  # True by definition
inf_is_greater = inf_positive > 1e308

# Float edge: large exponent literal
float_large = 1e308
float_scientific = 1.5e-10
float_with_separator = 1_000_000.0

# Complex values
complex_simple = 1j
complex_with_real = 2 + 3j
complex_pure_imag = 0j
complex_from_literal = complex(1, 2)
complex_conjugate = complex_with_real.conjugate()

# Negative floor division and modulo (floor semantics)
neg_floor = -7 // 3  # -3 (floor toward negative infinity)
neg_modulo = -7 % 3  # 2 (sign of divisor)
pos_floor_neg_divisor = 7 // -3  # -3
pos_modulo_neg_divisor = 7 % -3  # -2
floor_vs_trunc = (-7 // 3) != int(-7 / 3)  # floor vs truncation

# Exponent precedence
neg_exponent = -2**2  # -(2**2) = -4
parens_exponent = (-2)**2  # 4
right_associative = 2**3**2  # 2**(3**2) = 512
mixed_exponent = -2**3**2  # -(2**(3**2)) = -512

# Decimal and Fraction contrast vs float: valid-source structures for code-graph evaluation
import decimal
import fractions

decimal_one_tenth = decimal.Decimal("0.1")
decimal_two_tenths = decimal.Decimal("0.2")
decimal_sum = decimal_one_tenth + decimal_two_tenths  # Decimal("0.3") exact
float_sum = 0.1 + 0.2  # 0.30000000000000004 — not exact
decimal_vs_float_exactness = (decimal_sum == decimal.Decimal("0.3")) and (float_sum != 0.3)
fraction_half = fractions.Fraction(1, 2)
fraction_third = fractions.Fraction(1, 3)
fraction_sum = fraction_half + fraction_third  # 5/6 exact
fraction_vs_float = (fraction_sum == fractions.Fraction(5, 6)) and (float(1/2 + 1/3) != 5/6)
decimal_contrast_note = "decimal.Decimal preserves exact decimal; float does not"

# Leading-zero failure is excluded as invalid source; valid literals above have no leading zeros
# Valid zero is just 0, not 00 or 01

__all__ = [
    "hex_literal",
    "separated_decimal",
    "large_int",
    "inf_positive",
    "nan_not_equal_self",
    "complex_with_real",
    "neg_floor",
    "neg_modulo",
    "neg_exponent",
    "right_associative",
]
