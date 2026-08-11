/// A second part-owning library, this time using the legacy named `part of`
/// form on its part.
library fixture.parts.owner_named;

part 'owner_named_part.dart';

int _ownerNamedPrivateCounter = 0;

void bumpOwnerNamedCounter() {
  _ownerNamedPrivateCounter++;
}
