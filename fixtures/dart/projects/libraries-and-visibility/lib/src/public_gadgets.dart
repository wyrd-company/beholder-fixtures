library;

import 'internal_support.dart';

class BaseGadget {
  const BaseGadget(this.name);

  final String name;

  String describe() => '${InternalHelper.helperLabel()}:$name';
}

class ExtraGadget {
  const ExtraGadget(this.tag);

  final String tag;
}
