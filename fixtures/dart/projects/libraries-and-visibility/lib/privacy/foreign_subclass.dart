library;

import 'base_with_private_state.dart';

class ForeignSubclass extends StatefulBase {
  // Same text as `StatefulBase._state`, but private members are
  // library-scoped and not inherited across libraries: this is a distinct,
  // unrelated field with its own storage, not an override of the original.
  int _state = 100;

  int get foreignState => _state;
}
