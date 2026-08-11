/// Library whose part file inherits the package language version.
library versioned_library;

part 'versioned_library_part.dart';

/// Mutable holder used by the part extension.
class CounterHolder {
  int tally = 0;
}

/// Bumps the holder through the part extension.
int bumpCounter(CounterHolder holder) => holder.bump();
