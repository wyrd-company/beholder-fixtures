// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const decoratorLog: string[] = [];

function makeDecorator(label: string): any {
  return (_value: unknown, _context: unknown) => {
    decoratorLog.push(`decorator:${label}`);
  };
}

function makeFactory(label: string) {
  decoratorLog.push(`factory:${label}`);
  return makeDecorator(label);
}

@makeFactory("class-a")
@makeFactory("class-b")
export class DecoratedLedger {
  @makeFactory("field-a")
  fieldA = 1;

  @makeFactory("field-b")
  fieldB = 2;

  @makeFactory("method-a")
  methodA(): string {
    return "a";
  }

  @makeFactory("method-b")
  methodB(): string {
    return "b";
  }
}

export function decoratorOrder(): string[] {
  return [...decoratorLog];
}

export function resetDecoratorLog(): void {
  decoratorLog.length = 0;
}
