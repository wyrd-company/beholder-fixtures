"""String and bytes literal forms (PY-CAN-SRC-004).

Covers adjacent concatenation, raw/text/bytes prefixes, escapes, Unicode,
and quote processing. Text-bytes mixing and ASCII limits are demonstrated
through runtime contrasts rather than invalid source.
"""

# Adjacent concatenation — string literals separated only by whitespace concatenate
adjacent_simple = "hello " "world"
adjacent_mixed_quotes = "report " 'section ' """block"""
adjacent_across_lines = (
    "alpha "
    "beta "
    "gamma"
)
adjacent_with_parens = ("a" "b" "c")

# Raw, text, and bytes prefixes
raw_string = r"raw \n not newline \t tab \x41"
raw_with_backslash = r"ends with double backslash \\"
text_string = "text \n newline"
explicit_text_prefix = "explicit text"
bytes_literal = b"bytes \x41\x42"
bytes_with_escape = b"\x00\xff"
raw_bytes = br"raw bytes \n stays"
raw_bytes_reversed = rb"also raw bytes \t"

# Quote processing and triple-quoted forms
single_quoted = 'single'
double_quoted = "double"
triple_single = '''triple
single
still one string'''
triple_double = """triple
double
with "embedded" quotes"""
quoting_with_escape = "quote \"inside\" string"
quoting_single_in_double = "it's fine"
quoting_double_in_single = 'she said "hello"'

# Escapes
escaped_newline = "line\nnewline"
escaped_tab = "col1\ttab"
escaped_hex = "\x41\x42\x43"  # ABC
escaped_unicode_4 = "\u00e9"  # é
escaped_unicode_8 = "\U0001F600"  # grinning face
escaped_named = "\N{SNOWMAN}"  # ☃
escaped_octal = "\101"  # A in octal
escaped_backslash = "\\"
escaped_quote = "\""

# Unicode escapes in string vs raw difference
unicode_in_raw = r"\u00e9 stays literal in raw"
unicode_evaluated = "\u00e9 evaluates to é"

# Invalid escapes are excluded as invalid source; valid escapes above are exhaustive
# Evolution note: invalid escapes previously warned, now SyntaxError on newer Python.
# We keep only valid forms.

# Text-bytes mixing contrast — operation would fail at runtime, not syntax
text_value = "text"
bytes_value = b"bytes"
# Runtime guard demonstrating mixing would raise TypeError
mixing_raises = False
try:
    _ = text_value + bytes_value  # type: ignore[operator]
except TypeError:
    mixing_raises = True

# ASCII source limit for bytes: bytes literal may only contain ASCII characters
bytes_ascii_only = b"ascii only"
# Non-ASCII in bytes would be invalid; demonstrated by encoding text instead
unicode_as_bytes = "café".encode("utf-8")

# String concatenation vs adjacent literal folding — adjacent is compile-time
compile_time_adjacent = "a" "b"  # folded at parse time
runtime_concat = "a" + "b"  # runtime addition

__all__ = [
    "adjacent_simple",
    "raw_string",
    "bytes_literal",
    "raw_bytes",
    "triple_single",
    "escaped_hex",
    "escaped_unicode_4",
    "escaped_named",
    "mixing_raises",
    "unicode_as_bytes",
]
