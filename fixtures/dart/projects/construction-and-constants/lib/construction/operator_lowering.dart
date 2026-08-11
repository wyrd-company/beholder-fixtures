/// Implicit operator lowering fixtures for [DART-CAN-OBJ-006]: `a[i] +=
/// value`, property `??=` behind a getter and a conditional setter,
/// increment/decrement over a user-defined `+`/`-` operator, and single
/// evaluation of a side-effecting receiver and index.
library;

class Ledger {
  final Map<String, int> _balances = <String, int>{};

  int operator [](String key) => _balances[key] ?? 0;

  void operator []=(String key, int value) => _balances[key] = value;
}

class Profile {
  String? _nickname;

  String? get nickname => _nickname;

  set nickname(String? value) => _nickname = value;
}

class Meters {
  const Meters(this.value);

  final double value;

  Meters operator +(num delta) => Meters(value + delta);

  Meters operator -(num delta) => Meters(value - delta);

  @override
  String toString() => '${value}m';
}

class Track {
  Track(this.distance);

  Meters distance;
}

class Grid {
  final Map<int, int> _cells = <int, int>{};

  int operator [](int index) => _cells[index] ?? 0;

  void operator []=(int index, int value) => _cells[index] = value;
}

int receiverEvaluations = 0;
int indexEvaluations = 0;
final Grid _sharedGrid = Grid();

Grid _sideEffectingReceiver() {
  receiverEvaluations += 1;
  return _sharedGrid;
}

int _sideEffectingIndex() {
  indexEvaluations += 1;
  return 0;
}

List<String> describeOperatorLowering() {
  final ledger = Ledger();
  ledger['gold'] = 5;
  // `[]=` desugars to: ledger[]=('gold', ledger[]('gold') + 10).
  ledger['gold'] += 10;

  final profile = Profile();
  profile.nickname ??= 'anon';
  profile.nickname ??= 'ignored-because-already-set';

  final track = Track(const Meters(10));
  track.distance++;
  track.distance--;
  track.distance--;

  receiverEvaluations = 0;
  indexEvaluations = 0;
  _sideEffectingReceiver()[_sideEffectingIndex()] += 10;

  return <String>[
    'a[i] += value on Ledger: gold=${ledger['gold']}',
    'Property ??= reads via getter then conditionally writes via setter: '
        'nickname=${profile.nickname}',
    'Increment/decrement over user-defined + and -: distance=${track.distance}',
    'Side-effecting receiver and index each evaluate exactly once for a '
        'compound index assignment: receiverEvaluations=$receiverEvaluations, '
        'indexEvaluations=$indexEvaluations, cell=${_sharedGrid[0]}',
  ];
}
