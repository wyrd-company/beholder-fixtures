// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Auto-accessor field: `accessor` keyword creates hidden backing storage with
 * declaration and emitted getter/setter. Under TypeScript 5.9.3, ES2022 emits
 * private `#label_accessor_storage` fields with accessor pairs, ES2017 emits
 * WeakMap-backed helpers, and declaration emit retains the `accessor` keyword.
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
