// @dart=2.17
/// Post-super-parameter constructor forwarding with identical intent.
library post_super_params;

class BaseSlot {
  const BaseSlot(this.number);

  final int number;
}

class SuperForwardedSlot extends BaseSlot {
  SuperForwardedSlot(super.number);
}
