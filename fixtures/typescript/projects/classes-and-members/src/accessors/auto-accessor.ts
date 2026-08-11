// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Auto-accessor field: `accessor` keyword creates hidden backing storage with
 * declaration and emitted getter/setter. Emit differs between modern target
 * (native `accessor` kept) and downlevel target (desugared to defineProperty).
 */
export class AutoAccessDemo {
  accessor label = "auto-init";

  accessor count = 1;

  // Static auto-accessor
  static accessor revision = "auto-rev";

  /** Access backing storage is hidden; public accessor is the API. */
  describe(): string {
    return `${this.label}:${this.count}`;
  }
}

export class AutoAccessWithOverride extends AutoAccessDemo {
  override accessor label = "derived-auto";
}

export function exerciseAutoAccessor(): void {
  const a = new AutoAccessDemo();
  a.label = "hello";
  const l: string = a.label;
  a.count = 42;
  void l;
  AutoAccessDemo.revision = "r-99";
  void AutoAccessDemo.revision;
  void new AutoAccessWithOverride();
}
