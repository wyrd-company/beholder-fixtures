// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Comparison of decorator emit between the two regimes.
 *
 * Standard decorators (src/standard) emit via __esDecorate and
 * Symbol.metadata with context objects; they do not emit
 * __metadata("design:type") / "design:paramtypes" / "design:returntype".
 *
 * Legacy decorators (this directory) emit via __decorate and
 * __metadata("design:*") / __param when experimentalDecorators and
 * emitDecoratorMetadata are enabled. This file documents the comparison
 * and provides a legacy baseline for code-graph differentiation.
 *
 * Standard emit example (dist/standard/class-decorators.js):
 *   __esDecorate(null, _classDescriptor = { value: _classThis }, [_decorator], { kind: "class", name: ... , metadata: _metadata }, ...)
 *   if (_metadata) Object.defineProperty(_classThis, Symbol.metadata, { value: _metadata })
 *
 * Legacy emit example (dist/legacy/class-decorators.js):
 *   let Foo = class Foo { ... };
 *   Foo = __decorate([sealed, __metadata("design:paramtypes", [String, Number])], Foo);
 *   __decorate([readonly, __metadata("design:type", String)], Foo.prototype, "field", void 0);
 *   __decorate([logged, __param(0, required), __metadata("design:type", Function), __metadata("design:paramtypes", [String]), __metadata("design:returntype", String)], Foo.prototype, "method", null);
 *
 * Annotation-derived runtime constructor references are observable only
 * in the legacy emit through design:paramtypes arrays containing imported
 * constructors like CatalogItem. The standard emit retains no such
 * design:* metadata; constructor references are explicit values only where
 * the decorator author writes them.
 */

import { CatalogItem } from "./catalog-item.js";

function legacyTag(_constructor: Function): void {}

@legacyTag
export class ComparisonLegacy {
  constructor(public readonly item: CatalogItem) {}

  handle(value: string): string {
    return value;
  }
}

export const comparisonNote =
  "Standard decorators use Symbol.metadata and typed context; legacy decorators use __metadata design:* emit. See emitted JS in dist/standard versus dist/legacy.";
