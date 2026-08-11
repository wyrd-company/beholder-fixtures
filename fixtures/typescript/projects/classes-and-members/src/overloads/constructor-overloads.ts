// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Ordered constructor overloads with protected/private construction variants handled in static-side module. */
export class Crate {
  readonly label: string;
  readonly count: number;

  constructor(label: string);
  constructor(label: string, count: number);
  constructor(label: string, count?: number, ...extras: string[]);
  constructor(label: string, count?: number, ...extras: string[]) {
    this.label = extras.length > 0 ? `${label}:${extras.join("-")}` : label;
    this.count = count ?? 0;
  }
}

export class Tag {
  readonly id: string;
  readonly ns?: string;
  constructor(id: string);
  constructor(id: string, ns: string);
  constructor(id: string, ns?: string) {
    this.id = id;
    this.ns = ns;
  }
}

export function exerciseConstructorOverloads(): void {
  const a = new Crate("alpha");
  const b = new Crate("alpha", 3);
  const c = new Crate("alpha", 3, "x", "y");

  const t1 = new Tag("one");
  const t2 = new Tag("one", "ns");

  // Return type is the instance type Crate/Tag; overload resolution picks the matching signature.
  const _checkA: Crate = a;
  const _checkB: Tag = t1;
  void _checkA;
  void _checkB;
  void c;
  void t2;
}
