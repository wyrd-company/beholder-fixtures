library;

// `label` reaches this file through two re-export paths that both trace back
// to the same declaration in `collision_a.dart`. That is not ambiguous,
// unlike two distinct declarations sharing a name.
import 'diamond_export_left.dart';
import 'diamond_export_right.dart';

String describeDiamondExportConsumer() => label();
