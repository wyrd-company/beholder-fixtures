// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class StaticAccess {
  private static _revision = "r1";

  static get revision(): string {
    return this._revision;
  }

  static set revision(v: string) {
    this._revision = v;
  }

  static describe(): string {
    return this.revision;
  }
}

export class StaticReadonly {
  private static _token = "tok";

  static get token(): string {
    return this._token;
  }
  // No setter: static getter-only readonly inference
}

export function exerciseStaticAccessor(): void {
  StaticAccess.revision = "r2";
  const r: string = StaticAccess.revision;
  const t: string = StaticReadonly.token;
  void r;
  void t;
}
