library;

// Same text (`_secretName`) as the private top-level function in
// `private_members.dart`, but privacy is library-scoped: these are two
// unrelated declarations that happen to share spelling.
String _secretName() => 'from-other-private';

String describeOtherPrivateSecret() => _secretName();
