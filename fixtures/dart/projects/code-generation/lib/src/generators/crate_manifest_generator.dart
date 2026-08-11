import 'package:analyzer/dart/element/element.dart';
import 'package:build/build.dart';
import 'package:source_gen/source_gen.dart';

import '../annotations.dart';
import 'naming.dart';

/// Emits a standalone generated library describing each class annotated
/// with [CrateManifest], as resolved by `crateManifestBuilder`.
///
/// Unlike [ToolSummaryGenerator]'s `part` output, the emitted code is its own
/// library: it must import the annotated class's library explicitly, and any
/// private declaration it introduces is scoped to the generated file alone,
/// invisible even to the annotated class's own library.
class CrateManifestGenerator extends GeneratorForAnnotation<CrateManifest> {
  const CrateManifestGenerator();

  @override
  String generateForAnnotatedElement(
    Element element,
    ConstantReader annotation,
    BuildStep buildStep,
  ) {
    if (element is! ClassElement) {
      throw InvalidGenerationSourceError(
        '@CrateManifest can only annotate classes.',
        element: element,
      );
    }

    final className = element.name!;
    final libraryUri = buildStep.inputId.uri;
    final fields = element.fields.where((field) => !field.isStatic).toList();
    final idMatches = fields.where((field) => field.name == 'crateId');
    final capacityMatches = fields.where((field) => field.name == 'capacity');
    final idFieldName =
        (idMatches.isEmpty ? fields.first : idMatches.first).name!;
    final capacityFieldName =
        (capacityMatches.isEmpty ? fields.first : capacityMatches.first).name!;
    final privateHelperName =
        '_${className[0].toLowerCase()}${className.substring(1)}Label';
    final nameParts = splitPascalCase(
      className,
    ).map((part) => "  '$part',").join('\n');
    final namePartsName =
        '_${className[0].toLowerCase()}${className.substring(1)}NameParts';

    return '''
import '$libraryUri';

/// Private to this generated library: not reachable from
/// `${buildStep.inputId.path}` or any other file, even though that file
/// declares [$className] and this function's own annotation is read from it.
String $privateHelperName($className crate) => 'crate-\${crate.$idFieldName}';

/// Public façade over the generated crate description, reachable by any
/// importer of this standalone generated library.
String describe$className($className crate) =>
    '\${$privateHelperName(crate)} (capacity \${crate.$capacityFieldName})';

/// $className's name parts, generated with a source trailing comma
/// (DART-CAN-BUILD-004 formatter-style contrast). This library formats
/// under this generator's explicit `@dart=3.6` header override, under which
/// `dart format` treats a source trailing comma as a signal to keep a
/// same-line-eligible list split across lines, so this list stays split.
/// Compare `tool_record.g.dart`'s identically-shaped `_torqueWrenchNameParts`,
/// generated at the package's current default language version, where the
/// same trailing comma does not prevent the list from collapsing onto one
/// line.
const List<String> $namePartsName = [
$nameParts
];

/// Joins $namePartsName, so the formatter-style contrast list above is
/// generated content actually reachable from $className, not dead code.
String describe${className}NameParts() => $namePartsName.join(' ');
''';
  }
}
