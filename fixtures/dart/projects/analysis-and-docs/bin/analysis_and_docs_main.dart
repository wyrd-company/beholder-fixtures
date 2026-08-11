import 'package:analysis_and_docs/analysis_and_docs.dart';

void main() {
  final item = CatalogItem('w-1', 'Bracket', 2);
  final bin = SupplyBin('main', [item]);
  final inventory = DocumentedInventory([item]);
  print('bin total: ${bin.totalQuantity()}');
  print('first: ${inventory.firstItem()?.describe()}');
  print('generated: ${GeneratedSample.tag()}');
  print('record: ${inventory.makeRecord(item)}');
  print('use result: ${consumeUseResult(item)}');
  print('closure: ${makeAdder(3)(4)}');
  print('extension: ${'workshop'.truncated(4)}');
}
