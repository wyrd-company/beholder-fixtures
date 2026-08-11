/// The first of two libraries that share a documentary (legacy) library name.
/// The shared name is purely documentary: each library is identified by its
/// own URI, not by this name, so the two coexist without conflict.
library fixture.identity.shared;

String sharedNameLabel() => 'alpha';
