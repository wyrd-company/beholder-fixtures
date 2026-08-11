// strictPropertyInitialization: definite initialization is gated.
// With the flag on, properties must be initialized in the constructor or with definite assignment assertions.

export class Ledger {
  token: string;
  amount: number = 0;

  constructor(token: string) {
    this.token = token;
  }

  describe(): string {
    return `${this.token}:${this.amount}`;
  }
}

export class InitializedWithAssertion {
  // Definite assignment assertion satisfies strictPropertyInitialization when
  // initialization is performed outside the constructor.
  label!: string;

  initialize(label: string): void {
    this.label = label;
  }
}
