library;

// A legal import cycle: `mutual_a` imports `mutual_b`, which imports
// `mutual_a` back. Import cycles are legal (unlike inference or constant
// cycles, which remain errors).
import 'mutual_b.dart';

class NodeA {
  NodeB? partner;

  String describe() => 'A(${partner?.describe() ?? 'none'})';
}
