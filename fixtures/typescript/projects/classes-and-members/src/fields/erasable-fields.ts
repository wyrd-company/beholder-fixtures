// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Valid erasable forms subset of TS-CAN-050 that passes under `erasableSyntaxOnly: true`.
 * Contains only syntax that erases cleanly: typed fields, declare, and definite assignment
 * without emitting values that require transformation like parameter properties or `accessor`.
 */
export class ErasableBase {
  initialized = "base";

  definite!: string;

  declare declaredOnly: string;

  optional?: string;

  private _value = "backing";

  get value(): string {
    return this._value;
  }

  set value(v: string) {
    this._value = v;
  }
}

export class ErasableDerived extends ErasableBase {
  derivedInitialized = "derived";

  declare derivedDeclared: string;

  constructor(label: string) {
    super();
    this.definite = label;
  }
}
