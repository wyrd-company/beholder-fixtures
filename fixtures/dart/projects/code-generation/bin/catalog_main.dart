import 'package:toolshed_catalog/toolshed_catalog.dart';

void main() {
  const wrench = TorqueWrench('torque wrench ', 42.5);
  print(wrench.summary());
  print(wrench.nameLabel());

  const crate = StorageCrate('bench-1', 12);
  print(describeStorageCrate(crate));
  print(describeStorageCrateNameParts());

  print(
    '$benchCatalogCrateId: ${benchCatalogTools.map((tool) => tool.description).join(', ')}',
  );

  final tools = NativeTextTools();
  print('measured length: ${tools.measuredLength('torque wrench')}');
  print('rounded: ${tools.roundToNearest(3.5)}');

  print(describeStableGeneration());
}
