// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Base class with initialized and uninitialized fields, setter, declare, and definite assignment. */
export class BaseFields {
  /** Initialized field. */
  initialized = "base-init";

  /** Uninitialized field with definite assignment assertion. */
  definite!: string;

  /** Declare field: no emit, erased type-only property declaration. */
  declare declaredField: string;

  /** Uninitialized optional field. */
  optional?: string;

  private _shadowed = "base-setter-backing";

  get shadowed(): string {
    return this._shadowed;
  }

  set shadowed(value: string) {
    this._shadowed = value;
  }

  constructor() {
    this.definite = "assigned-in-ctor";
  }
}
