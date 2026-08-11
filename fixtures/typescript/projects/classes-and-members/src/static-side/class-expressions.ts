// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Anonymous and named class expressions passed or returned as values. */

export function makeAnonymousClass(label: string) {
  return class {
    label = label;
    describe(): string {
      return this.label;
    }
  };
}

export function makeNamedClassExpression(tag: string) {
  const Named = class NamedClass {
    tag = tag;
    describe(): string {
      return `${Named.name}:${this.tag}`;
    }
  };
  return Named;
}

export function consumeClass(ctor: new () => { describe(): string }): string {
  return new ctor().describe();
}

export function exerciseClassExpressions(): void {
  const AnonCls = makeAnonymousClass("anon");
  const a = new AnonCls();
  void a.describe();

  const NamedCls = makeNamedClassExpression("named");
  const n = new NamedCls();
  void n.describe();

  // Positional identity: two anonymous class expressions produce distinct types even if structurally equal.
  const AnonA = makeAnonymousClass("a");
  const AnonB = makeAnonymousClass("b");
  void new AnonA();
  void new AnonB();

  // Passed as value
  void consumeClass(AnonCls);
  void consumeClass(NamedCls);

  // Returned as value
  void makeAnonymousClass("returned");
}
