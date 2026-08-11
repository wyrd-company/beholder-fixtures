// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Same shape with different visibility modifiers; demonstrates protected/private assignability. */
export class PublicBase {
  public value = "public";
  public describe(): string {
    return this.value;
  }
}

export class ProtectedBase {
  protected value = "protected";
  protected describe(): string {
    return this.value;
  }
}

export class SoftPrivateBase {
  private value = "soft-private";
  private describe(): string {
    return this.value;
  }

  reveal(): string {
    return this.value;
  }
}

export class HardPrivateBase {
  #value = "hard-private";
  getValue(): string {
    return this.#value;
  }
  setValue(v: string): void {
    this.#value = v;
  }

  /** Brand check via `#value in obj` narrowing. */
  hasHardValue(obj: unknown): boolean {
    return #value in (obj as HardPrivateBase);
  }
}

/** Subclass can access protected members of base but not private. */
export class ProtectedDerived extends ProtectedBase {
  expose(): string {
    return this.value; // protected access allowed in subclass
  }

  describeViaSuper(): string {
    return this.describe();
  }
}

export class PublicDerived extends PublicBase {
  expose(): string {
    return this.value;
  }
}

export function exerciseVisibility(): void {
  const pub = new PublicDerived();
  void pub.value; // public accessible everywhere

  const prot = new ProtectedDerived();
  void prot.expose();

  const soft = new SoftPrivateBase();
  void soft.reveal();
  // soft.value is not accessible outside class (soft-private).

  const hard = new HardPrivateBase();
  void hard.getValue();
  void hard.hasHardValue(new HardPrivateBase());

  // Declaration emit for each visibility form is present in `dist/visibility/*.d.ts`
}
