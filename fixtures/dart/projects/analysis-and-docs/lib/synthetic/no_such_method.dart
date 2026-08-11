/// `noSuchMethod` forwarders for DART-CAN-DIAG-008.
library;

/// Interface that is implemented via `noSuchMethod` forwarders.
abstract class WorkshopOps {
  String labelOf(String id);
  void store(String id, int count);
}

/// Class that implements the interface via a catch-all forwarder.
class DynamicWorkshop implements WorkshopOps {
  @override
  dynamic noSuchMethod(Invocation invocation) {
    final name = invocation.memberName;
    if (name == #labelOf) {
      final id = invocation.positionalArguments.first as String;
      return 'label:$id';
    }
    if (name == #store) {
      return null;
    }
    return super.noSuchMethod(invocation);
  }
}

// Observable forwarder behavior via dynamic invocation.
String useNoSuchMethod() {
  final WorkshopOps ops = DynamicWorkshop();
  return ops.labelOf('w-1');
}
