/// Canonicalization and identity fixtures for [DART-CAN-CONST-002]:
/// repeated equal const objects, collections, records, and symbols compared
/// with `identical`; a cross-library const reference compared with a
/// non-const instance; a const factory redirect; and generic instantiation.
///
/// The deferred-load-unit const-identity corner named alongside this item is
/// owned by `libraries-and-visibility` and `platforms-and-interop` and is not
/// reproduced here.
library;

import '../construction/shape_factory.dart';
import 'basics.dart';
import 'shared_values.dart' as shared;

const Money localZeroMoney = Money(0);
final Money nonConstZeroMoney = Money(0);

const List<int> listA = <int>[1, 2];
const List<int> listB = <int>[1, 2];

const (int, String) recordA = (1, 'a');
const (int, String) recordB = (1, 'a');

const Wrapper<int> wrapperIntA = Wrapper<int>(7);
const Wrapper<int> wrapperIntB = Wrapper<int>(7);
const Wrapper<num> wrapperNum = Wrapper<num>(7);

List<String> describeCanonicalization() {
  return <String>[
    'Repeated equal const objects canonicalize: '
        'identical(localZeroMoney, const Money(0))=${identical(localZeroMoney, const Money(0))}',
    'Const collections canonicalize: identical(listA, listB)=${identical(listA, listB)}',
    'Const records canonicalize: identical(recordA, recordB)=${identical(recordA, recordB)}',
    'Const symbols canonicalize: identical(#answer, #answer)=${identical(#answer, #answer)}',
    'Cross-library const reference canonicalizes with a locally declared '
        'equal const: identical(shared.originMoney, localZeroMoney)='
        '${identical(shared.originMoney, localZeroMoney)}',
    'A const value is not identical to an equal non-const instance: '
        'identical(localZeroMoney, nonConstZeroMoney)='
        '${identical(localZeroMoney, nonConstZeroMoney)}',
    'const factory redirect canonicalizes with its target: '
        'identical(Coord.zero(), Coord(0,0))=${identical(const Coord.zero(), const Coord(0, 0))}',
    'Generic instantiation canonicalizes by reified type argument: '
        'identical(Wrapper<int>(7), Wrapper<int>(7))=${identical(wrapperIntA, wrapperIntB)}, '
        'identical(Wrapper<int>(7), Wrapper<num>(7))=${identical(wrapperIntA, wrapperNum)}',
  ];
}
