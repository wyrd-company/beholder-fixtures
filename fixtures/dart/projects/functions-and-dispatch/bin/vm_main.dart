import 'dart:io';

import 'package:functions_and_dispatch/checks/check_support.dart';
import 'package:functions_and_dispatch/kinds/capture.dart';
import 'package:functions_and_dispatch/kinds/function_forms.dart';
import 'package:functions_and_dispatch/symbols/symbol_observability.dart';
import 'package:functions_and_dispatch/types/function_types.dart';
import 'package:functions_and_dispatch/types/tear_offs.dart';

/// The default (`vm-jit`) synchronous entry point. It exercises
/// function kinds, capture, function types, tear-offs, and symbols; the
/// asynchronous entry library `vm_async_main.dart` exercises dynamic
/// dispatch and entry-point-specific coverage.
void main(List<String> arguments) {
  stdout.writeln('vm-jit sync entry ran with ${arguments.length} arguments');
  _runFunctionKinds();
  _runCapture();
  _runFunctionTypes();
  _runTearOffs();
  _runSymbols();
  stdout.writeln('vm-jit vm_main checks passed');
}

void _runFunctionKinds() {
  expectEqual(addTopLevel(2, 3), 5, 'addTopLevel');
  expectEqual(multiplyTopLevel(2, 3), 6, 'multiplyTopLevel');
  expectEqual(
    describeReading('sensor', 10),
    'sensor reads 10 units',
    'describeReading default unit',
  );
  expectEqual(
    describeReading('sensor', 10, 'C'),
    'sensor reads 10 C',
    'describeReading explicit unit',
  );
  expectEqual(
    labelReading('sensor', 10, category: 'temp'),
    'temp: sensor=10',
    'labelReading default approximate',
  );
  expectEqual(
    labelReading('sensor', 10, category: 'temp', approximate: true),
    'temp: sensor=~10',
    'labelReading approximate',
  );
  expectEqual(
    callLabelReadingWithInterleavedNamedArgument(),
    'temperature: sensor=41',
    'callLabelReadingWithInterleavedNamedArgument',
  );

  readingLog.clear();
  logReading('calibrated');
  expectList(readingLog, ['calibrated'], 'logReading');

  var rejected = false;
  try {
    rejectReading('out of range');
  } on StateError {
    rejected = true;
  }
  expectTrue(rejected, 'rejectReading throws');

  final station = ReadingStation('north');
  expectEqual(station.adjustedReading(3), 14, 'adjustedReading');
  expectEqual(
    ReadingStation.calibrationOffset(3),
    5,
    'calibrationOffset static',
  );
  expectList(station.doubledReadings([1, 2, 3]), [2, 4, 6], 'doubledReadings');
}

void _runCapture() {
  final counter = makeCounter(10);
  expectEqual(counter(), 11, 'makeCounter first');
  expectEqual(counter(), 12, 'makeCounter second');

  expectList(mutateAfterCapture(), [41, 41], 'mutateAfterCapture');

  expectEqual(makeFactorial()(5), 120, 'makeFactorial');

  final closures = captureEachIteration();
  expectEqual(closures[0](), 0, 'captureEachIteration[0]');
  expectEqual(closures[1](), 1, 'captureEachIteration[1]');
  expectEqual(closures[2](), 2, 'captureEachIteration[2]');
}

void _runFunctionTypes() {
  expectEqual(addStructural(2, 3), 5, 'addStructural');
  final BinaryOp op = selectAddStructural();
  expectEqual(op(2, 3), 5, 'selectAddStructural');

  expectEqual(identityTransform<int>(5), 5, 'identityTransform');
  final Transformer t = selectIdentityTransformer();
  expectEqual(t<int>(5), 5, 'selectIdentityTransformer');

  const multiplier = Multiplier(3);
  expectEqual(multiplier(4), 12, 'Multiplier.call');
  final UnaryOp coerced = coerceCallableToFunctionType(multiplier);
  expectEqual(coerced(4), 12, 'coerceCallableToFunctionType');

  final anyDescription = describeAnyFunction(addStructural);
  expectTrue(anyDescription.isNotEmpty, 'describeAnyFunction non-empty');

  const animal = Animal('Rex');
  final revived = reviveAsDog(animal);
  expectEqual(revived.name, 'Rex', 'reviveAsDog');
  final AnimalHandler handler = pickHandler();
  expectEqual(handler(const Dog('Fido')).name, 'Fido', 'pickHandler');
}

void _runTearOffs() {
  expectEqual(tearOffTopLevel()(4), 16, 'tearOffTopLevel');
  expectEqual(tearOffStatic()(3), 27, 'tearOffStatic');

  const toolkit = MathToolkit(5);
  expectEqual(tearOffBound(toolkit)(10), 15, 'tearOffBound');
  expectEqual(tearOffGeneric(toolkit)<int>(9), 9, 'tearOffGeneric');
  expectEqual(tearOffExtension(7)(), 'number(7)', 'tearOffExtension');

  final comparison = compareGetterAndMethod(toolkit);
  expectEqual(comparison.getterInvoked, 13, 'GetterVersusMethod getter');
  expectEqual(comparison.methodInvoked, 8, 'GetterVersusMethod method');

  final tearOffComparison = compareTearOffs(toolkit);
  expectTrue(
    tearOffComparison.topLevelIdentical,
    'top-level tear-off identity',
  );
  expectTrue(tearOffComparison.staticIdentical, 'static tear-off identity');
  expectTrue(tearOffComparison.boundEqual, 'bound tear-off equality');
}

void _runSymbols() {
  expectTrue(
    symbolLiteralEqualsConstructed(),
    'symbolLiteralEqualsConstructed',
  );
  expectTrue(constructedSymbolsAreEqual(), 'constructedSymbolsAreEqual');
  expectTrue(
    privateSymbolsFromSameLibraryAreEqual(),
    'privateSymbolsFromSameLibraryAreEqual',
  );
  expectEqual(
    applyWithConstructedSymbol('hello'),
    10,
    'applyWithConstructedSymbol',
  );
  expectEqual(describeLength('hello'), 5, 'describeLength default measure');
}
