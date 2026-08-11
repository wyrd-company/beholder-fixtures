// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Overloaded constructors with InstanceType and construction visibility. */

export class MultiCtor {
  label: string;
  count: number;

  constructor(label: string);
  constructor(label: string, count: number);
  constructor(label: string, count?: number) {
    this.label = label;
    this.count = count ?? 0;
  }
}

export class ProtectedCtor {
  protected constructor(public readonly token: string) {}

  static create(token: string): ProtectedCtor {
    return new ProtectedCtor(token);
  }
}

export class PrivateCtor {
  private constructor(public readonly id: string) {}

  static factory(id: string): PrivateCtor {
    return new PrivateCtor(id);
  }
}

/** Subclassing private constructor is not demonstrated as invalid source; comment notes it. */

export class SubclassProtectedCtor extends ProtectedCtor {
  constructor(
    token: string,
    public extra: string,
  ) {
    super(token);
  }
}

export type MultiCtorInstance = InstanceType<typeof MultiCtor>;

export function exerciseOverloadedConstructors(): void {
  const a = new MultiCtor("alpha");
  const b = new MultiCtor("alpha", 3);
  void a.label;
  void b.count;

  const viaInstanceType: MultiCtorInstance = new MultiCtor("via");
  void viaInstanceType;

  // External `new` is allowed via public static factory for private/protected construction
  const p = ProtectedCtor.create("prot");
  const q = PrivateCtor.factory("priv");
  void p.token;
  void q.id;

  const sub = new SubclassProtectedCtor("prot", "extra");
  void sub.extra;

  // Singleton/factory pattern uses private construction internally.
}
