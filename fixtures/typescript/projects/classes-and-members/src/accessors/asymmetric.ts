// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Asymmetric read/write types:
 * - TS 4.3: setter parameter type may be wider than getter return type.
 * - TS 5.1: getter and setter types may be explicitly unrelated.
 */
export class AsymmetricAccess {
  private _value: string | number = "init";

  // Getter returns string, setter accepts string | number (wider) – valid since 4.3
  get value(): string {
    return String(this._value);
  }

  set value(v: string | number) {
    this._value = v;
  }
}

export class UnrelatedAccess {
  private _payload: string = "payload";

  // Explicitly unrelated read/write types: getter string, setter number (5.1)
  get payload(): string {
    return this._payload;
  }

  set payload(v: number) {
    this._payload = String(v);
  }
}

export function exerciseAsymmetric(): void {
  const a = new AsymmetricAccess();
  const read: string = a.value; // read type string
  a.value = 42; // write accepts number
  a.value = "hello";
  void read;

  const u = new UnrelatedAccess();
  const r: string = u.payload;
  u.payload = 99;
  void r;
}
