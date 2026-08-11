// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Arrow lexical this versus ordinary function/method dynamic this. */
export class LexicalHolder {
  name = "lexical";
  arrow = (): string => this.name;

  method(): string {
    return this.name;
  }

  ordinaryFunction(): string {
    function inner(this: LexicalHolder): string {
      return this.name;
    }
    // .call provides the correct this
    return inner.call(this);
  }
}

export function exerciseLexicalThis(): void {
  const holder = new LexicalHolder();
  const arrowResult: string = holder.arrow();
  const methodResult: string = holder.method();
  const ordinaryResult: string = holder.ordinaryFunction();
  void arrowResult;
  void methodResult;
  void ordinaryResult;
}
