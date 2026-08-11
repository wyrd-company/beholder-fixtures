library;

import 'chain_leaf.dart';
import 'diamond_top.dart';
import 'cycle_a.dart';

String describeFacadeConsumer() {
  final chained = BaseGadget('chain').describe();
  final diamond = BaseGadget('diamond').describe();
  final cycled = ExtraGadget('cycle').tag;
  return '$chained/$diamond/$cycled';
}
