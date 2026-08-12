// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** extends of a class-producing expression and implements-erased vs extends-runtime edge. */

export function baseFactory(tag: string) {
  return class BaseWithTag {
    tag = tag;
    label(): string {
      return this.tag;
    }
  };
}

/** The `extends` clause directly contains the class-producing call expression. */
export class DerivedFromExpression extends baseFactory("factory-tag") {
  extra = "derived";

  describe(): string {
    return `${this.label()}:${this.extra}`;
  }
}

/** Implements is erased; extends has runtime effect. */
export interface ErasedContract {
  token(): string;
}

export class ImplementsErased implements ErasedContract {
  token(): string {
    return "erased-token";
  }
  // No runtime heritage from the interface; `instanceof` check is not meaningful.
}

export const RuntimeBase = baseFactory("runtime-tag");

export class ExtendsRuntime extends RuntimeBase {
  token(): string {
    return this.label();
  }
}

export function exerciseExpressionExtends(): void {
  const d = new DerivedFromExpression();
  const e = new ImplementsErased();
  const r = new ExtendsRuntime();
  void d.describe();
  void e.token();
  void r.token();

  // `implements` does not create a runtime prototype chain, `extends` does:
  const isInstance = r instanceof RuntimeBase;
  void isInstance;

  // Separate factory call produces a distinct constructor, not the same prototype chain:
  const OtherBase = baseFactory("runtime-tag");
  void (r instanceof (OtherBase as unknown as abstract new () => unknown));
}
