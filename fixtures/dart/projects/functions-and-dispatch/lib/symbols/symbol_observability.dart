/// Symbol literals, `Symbol` construction for use as `Function.apply`
/// named-argument keys, private-name symbols, and symbol equality.
///
/// Runtime name strings observed here (via [Symbol.toString] or
/// [Type.toString]) are recorded, not asserted as portable across
/// backends: this project declares only `vm-jit` and `native-aot`
/// contexts, neither of which minifies or obfuscates names, so the
/// observations below are stable within those contexts.
library;

/// A symbol literal.
const Symbol readingSymbol = #reading;

/// Constructs a [Symbol] from a runtime string rather than a literal.
Symbol symbolFromName(String name) => Symbol(name);

int describeLength(String value, {int Function(String)? measure}) =>
    (measure ?? (String s) => s.length)(value);

/// Applies [describeLength] through `Function.apply`, keying the named
/// `measure` argument with a [Symbol] built from a string via
/// [symbolFromName] rather than a `#measure` literal.
int applyWithConstructedSymbol(String value) {
  return Function.apply(
        describeLength,
        <String>[value],
        <Symbol, Object?>{
          symbolFromName('measure'): (String s) => s.length * 2,
        },
      )
      as int;
}

/// A symbol literal and an equivalent [Symbol] built from a string
/// compare equal.
bool symbolLiteralEqualsConstructed() => readingSymbol == Symbol('reading');

/// Two independently constructed symbols built from the same name
/// compare equal even though they are distinct expressions.
bool constructedSymbolsAreEqual() =>
    symbolFromName('same-name') == symbolFromName('same-name');

/// A private-name symbol literal, denoting a library-private name.
Symbol firstPrivateSymbolLiteral() => #_secretReading;

/// A second, independent occurrence of the same private-name symbol
/// literal.
Symbol secondPrivateSymbolLiteral() => #_secretReading;

/// Two private-name symbol literals for the same name, evaluated at
/// two different call sites within this library, compare equal.
bool privateSymbolsFromSameLibraryAreEqual() =>
    firstPrivateSymbolLiteral() == secondPrivateSymbolLiteral();
