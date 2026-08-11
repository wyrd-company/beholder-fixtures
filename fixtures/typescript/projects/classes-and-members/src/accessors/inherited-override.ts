// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class BaseWithAccess {
  private _name = "base";

  get name(): string {
    return this._name;
  }

  set name(v: string) {
    this._name = v;
  }
}

/** Inherited accessor override; property vs accessor override diagnostic is covered by comment. */
export class DerivedOverride extends BaseWithAccess {
  private _overrideTag = "derived";

  override get name(): string {
    return `${super.name}:${this._overrideTag}`;
  }

  override set name(v: string) {
    super.name = v;
  }
}

// Property overriding an accessor would be a diagnostic; valid override retains accessor kind.

export function exerciseInheritedOverride(): void {
  const d = new DerivedOverride();
  d.name = "hello";
  const n: string = d.name;
  void n;
}
