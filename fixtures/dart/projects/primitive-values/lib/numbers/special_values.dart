/// `NaN`, positive and negative infinity, and signed zero.
library;

List<String> describeSpecialValues() {
  const nan = double.nan;
  const positiveInfinity = double.infinity;
  const negativeInfinity = double.negativeInfinity;
  const positiveZero = 0.0;
  const negativeZero = -0.0;

  return <String>[
    'nan=$nan',
    'nan.isNaN=${nan.isNaN}',
    'nanEqualsSelf=${nan == nan}',
    'positiveInfinity=$positiveInfinity',
    'negativeInfinity=$negativeInfinity',
    'infinityFromDivision=${1.0 / 0.0}',
    'negativeInfinityFromDivision=${-1.0 / 0.0}',
    'zeroDividedByZeroIsNaN=${(0.0 / 0.0).isNaN}',
    'positiveZero=$positiveZero',
    'negativeZero=$negativeZero',
    'positiveZeroEqualsNegativeZero=${positiveZero == negativeZero}',
    'positiveZeroIdenticalNegativeZero='
        '${identical(positiveZero, negativeZero)}',
    'oneOverPositiveZero=${1.0 / positiveZero}',
    'oneOverNegativeZero=${1.0 / negativeZero}',
  ];
}
