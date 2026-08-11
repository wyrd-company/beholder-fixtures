/// Equality, identity, and hashing fixtures for [DART-CAN-CONST-003]: an
/// overridden `==` with a matching `hashCode`, `identical`, map and set
/// keys, records and enums as keys, and documented numeric and `NaN` cases.
///
/// Numeric identity and NaN identity can be implementation-defined across
/// backends, so this file records their observed values rather than
/// asserting a single portable outcome.
library;

class Currency {
  const Currency(this.code);

  final String code;

  @override
  bool operator ==(Object other) => other is Currency && other.code == code;

  @override
  int get hashCode => code.hashCode;

  @override
  String toString() => code;
}

enum Grade { a, b, c }

List<String> describeEqualityIdentityHashing() {
  const usdA = Currency('usd');
  final usdB = Currency('usd');

  final Map<Currency, int> rates = <Currency, int>{
    const Currency('usd'): 1,
    const Currency('eur'): 2,
  };
  final ratesLookupWithNonConstKey = rates[Currency('usd')];

  final Set<Currency> currencySet = <Currency>{const Currency('usd'), usdB};

  final Map<Grade, String> gradeLabels = <Grade, String>{
    Grade.a: 'excellent',
    Grade.b: 'good',
  };

  final Map<(int, String), String> recordKeyed = <(int, String), String>{
    (1, 'x'): 'value-for-1-x',
  };

  // Read through a variable rather than comparing the `double.nan` literal
  // directly, so the documented outcome is a runtime observation rather
  // than an analyzer-foldable always-false comparison.
  final double nanValue = double.nan;
  final bool nanEqualsSelf = nanValue == nanValue;
  final bool nanIdenticalSelf = identical(nanValue, nanValue);
  final bool intDoubleEqual = 1 == 1.0;
  final bool intDoubleIdentical = identical(1, 1.0);
  final bool signedZeroEqual = 0.0 == -0.0;
  final bool signedZeroIdentical = identical(0.0, -0.0);

  return <String>[
    'Overridden == with matching hashCode: usdA == usdB=${usdA == usdB}, '
        'hashCode match=${usdA.hashCode == usdB.hashCode}, '
        'identical(usdA, usdB)=${identical(usdA, usdB)}',
    'Map keys use == and hashCode, not identity: lookup with a non-const '
        'equal key finds the entry=${ratesLookupWithNonConstKey == 1}',
    'Set de-duplicates equal keys: currencySet.length=${currencySet.length}',
    'Enum as a map key: ${gradeLabels[Grade.a]}',
    'Record as a map key: ${recordKeyed[(1, 'x')]}',
    'Documented numeric and NaN cases (values recorded, not asserted '
        'portable): nanEqualsSelf=$nanEqualsSelf, '
        'nanIdenticalSelf=$nanIdenticalSelf, intDoubleEqual=$intDoubleEqual, '
        'intDoubleIdentical=$intDoubleIdentical, '
        'signedZeroEqual=$signedZeroEqual, '
        'signedZeroIdentical=$signedZeroIdentical',
  ];
}
