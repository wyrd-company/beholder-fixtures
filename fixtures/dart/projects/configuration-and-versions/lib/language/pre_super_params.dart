// @dart=2.16
/// Pre-super-parameter constructor forwarding.
library pre_super_params;

class BaseValue {
  const BaseValue(this.number);

  final int number;
}

class ForwardedValue extends BaseValue {
  ForwardedValue(int number) : super(number);
}
