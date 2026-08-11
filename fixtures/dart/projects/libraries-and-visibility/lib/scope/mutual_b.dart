library;

import 'mutual_a.dart';

class NodeB {
  NodeA? partner;

  String describe() => 'B(${partner?.describe() ?? 'none'})';
}
