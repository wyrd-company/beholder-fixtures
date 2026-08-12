// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Base class with initialized and uninitialized fields, declare, and definite assignment. */
export class BaseFields {
  /** Initialized field. */
  initialized = "base-init";

  /** Uninitialized field with definite assignment assertion. */
  definite!: string;

  /** Declare field: no emit, erased type-only property declaration. */
  declare declaredField: string;

  /** Uninitialized optional field. */
  optional?: string;

  _shadowedBacking = "base-setter-backing";

  constructor() {
    this.definite = "assigned-in-ctor";
  }
}

Object.defineProperty(BaseFields.prototype, "shadowed", {
  get(this: BaseFields): string {
    return (this as unknown as { _shadowedBacking: string })._shadowedBacking;
  },
  set(this: BaseFields, value: string) {
    (this as unknown as { _shadowedBacking: string })._shadowedBacking = value;
  },
  enumerable: true,
  configurable: true,
});

export interface BaseFields {
  shadowed: string;
}
