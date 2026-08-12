// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Legacy emitDecoratorMetadata: design:type, design:paramtypes,
 * design:returntype, annotation-derived constructor references,
 * lossy encodings, and import retention.
 *
 * The emitted JavaScript contains __metadata("design:type", ...),
 * __metadata("design:paramtypes", [...]), and
 * __metadata("design:returntype", ...) calls observable in dist/legacy.
 */

import { CatalogItem } from "./catalog-item.js";

function tracked(_target: Object, _propertyKey: string | symbol): void {}

function trackedClass(constructor: Function): void {}

function loggedType(
  _target: Object,
  _propertyKey: string | symbol,
  _descriptor: PropertyDescriptor,
): void {}

@trackedClass
export class MetadataDesignGallery {
  // design:type for property (String)
  @tracked
  title: string = "metadata-title";

  // design:type for property with imported constructor (CatalogItem)
  @tracked
  item: CatalogItem = new CatalogItem("sku-0", "zero");

  // design:type for numeric property (Number), design:paramtypes empty
  @tracked
  count: number = 0;

  // design:type Function, design:paramtypes [String], design:returntype String
  @loggedType
  describe(label: string): string {
    return label;
  }

  // design:paramtypes includes union lossy encoding (Object) for "string | number"
  // and imported type retention for CatalogItem.
  @loggedType
  withUnion(value: string | number, item: CatalogItem): string {
    return `${String(value)}:${item.sku}`;
  }

  // decorated accessor emits combined design:type Number and
  // design:paramtypes [Number]; no design:returntype is emitted for accessors
  @tracked
  get score(): number {
    return this.count;
  }

  set score(value: number) {
    this.count = value;
  }

  // design:paramtypes for constructor with imported and primitive types
  constructor(
    public readonly primary: CatalogItem,
    public readonly secondary: string,
    public readonly amount: number,
  ) {}
}

/**
 * Lossy encodings: generic types such as Array<string> emit as Array, while
 * unions such as string | number emit as Object. Annotation structure is not
 * fully preserved at runtime but produces observable metadata entries.
 */
export class LossyMetadataGallery {
  @tracked
  genericValue: Array<string> = [];

  @tracked
  unionValue: string | number = "sample";

  @tracked
  optionalValue?: string;

  @loggedType
  handleGeneric(items: Array<string>): Array<string> {
    return items;
  }

  @loggedType
  handleUnion(input: string | number): string | number {
    return input;
  }
}
