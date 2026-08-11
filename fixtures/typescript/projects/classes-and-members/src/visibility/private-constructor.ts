// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Private constructor: singleton / factory pattern; subclassing is prohibited. */
export class Singleton {
  private static _instance: Singleton | undefined;

  private constructor(public readonly id: string) {}

  static getInstance(id: string): Singleton {
    if (!Singleton._instance) Singleton._instance = new Singleton(id);
    return Singleton._instance;
  }

  static create(id: string): Singleton {
    return new Singleton(id);
  }
}

/** Factory using private construction internally. */
export class Token {
  private constructor(private readonly raw: string) {}

  static from(raw: string): Token {
    return new Token(raw);
  }

  value(): string {
    return this.raw;
  }
}

export function exercisePrivateConstructor(): void {
  const s = Singleton.getInstance("one");
  const t = Token.from("raw-token");
  void s.id;
  void t.value();
}
