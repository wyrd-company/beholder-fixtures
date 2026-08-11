// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Paired getter and setter with symmetric type. */
export class PairedAccess {
  private _label = "init";

  get label(): string {
    return this._label;
  }

  set label(value: string) {
    this._label = value;
  }
}

/** Getter-only: inferred readonly. */
export class GetterOnly {
  private _token = "token";

  get token(): string {
    return this._token;
  }
}

/** Setter-only: write-only property (no read). */
export class SetterOnly {
  private _count = 0;

  set count(value: number) {
    this._count = value;
  }

  getCount(): number {
    return this._count;
  }
}

export function exercisePaired(): void {
  const p = new PairedAccess();
  p.label = "hello";
  const read: string = p.label;
  void read;

  const g = new GetterOnly();
  const tok: string = g.token;
  // g.token = "x" would be rejected (readonly).
  void tok;

  const s = new SetterOnly();
  s.count = 42;
  void s.getCount();
}
