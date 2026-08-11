/// Single-line, multiline, and raw string literals, adjacent literal
/// concatenation, and escape sequences.
library;

const singleQuoted = 'single-quoted';
const doubleQuoted = "double-quoted";
const multiline = '''
first line
second line''';
const rawString = r'raw\nstring$withoutEscapes';
const adjacentConcatenation =
    'adjacent'
    ' '
    'literals';
const escaped =
    'tab:\tnewline:\ndollar:\$backslash:\\heart:❤braced:\u{1F600}hex:\x41';

List<String> describeStringLiterals() => <String>[
  'singleQuoted=$singleQuoted',
  'doubleQuoted=$doubleQuoted',
  'singleQuotedEqualsDoubleQuoted=${singleQuoted == 'single-quoted' && doubleQuoted == "double-quoted"}',
  'multiline=$multiline',
  'rawString=$rawString',
  'adjacentConcatenation=$adjacentConcatenation',
  'escaped=$escaped',
];
