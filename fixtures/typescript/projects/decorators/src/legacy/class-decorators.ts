// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Legacy class decorators under experimentalDecorators.
 * Demonstrates factories, ordering, and annotation-derived constructor
 * references via emitDecoratorMetadata (design:paramtypes).
 */

export const legacyClassLog: string[] = [];

function sealed(constructor: Function): void {
  legacyClassLog.push(`sealed:${constructor.name}`);
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

function tagged(tag: string) {
  return function (constructor: Function): void {
    legacyClassLog.push(
      `tagged:${String(tag)}:${(constructor as { name: string }).name}`,
    );
    (constructor as unknown as Record<string, unknown>).__tag = tag;
  };
}

function outerClass(constructor: Function): void {
  legacyClassLog.push(
    `apply:outerClass:${(constructor as { name: string }).name}`,
  );
}

function innerClass(constructor: Function): void {
  legacyClassLog.push(
    `apply:innerClass:${(constructor as { name: string }).name}`,
  );
}

@sealed
export class SealedCatalog {
  static kind = "sealed";
}

@tagged("ledger")
@tagged("archive")
export class TaggedLedger {
  static kind = "tagged";
}

@outerClass
@innerClass
export class OrderedLegacyCatalog {
  static kind = "ordered-legacy";
}

/**
 * Annotation-derived runtime constructor references.
 * `CatalogItem` import is retained in emit because design:paramtypes
 * references the imported constructor at runtime.
 */
import { CatalogItem } from "./catalog-item.js";

@tagged("with-paramtypes")
export class ServiceWithParamTypes {
  constructor(
    public readonly item: CatalogItem,
    public readonly count: number,
  ) {}
}

@tagged("no-params")
export class EmptyService {
  constructor() {}
}

export function getLegacyClassLog(): string[] {
  return [...legacyClassLog];
}
