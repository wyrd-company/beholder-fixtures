// Target-dependent class-field default: useDefineForClassFields defaults to false under ES5/ES2021 and true under ES2022+.
// Same source shows define-semantics versus assign-semantics in emit.

export class Vault {
  token: string = "default-token";
  count: number = 0;

  constructor(token?: string) {
    if (token) {
      this.token = token;
    }
  }

  describe(): string {
    return `${this.token}:${this.count}`;
  }
}

export class DerivedVault extends Vault {
  override token = "derived-token";
  extra: string = "extra";

  constructor() {
    super("base-token");
  }
}

export function createVault(token: string): Vault {
  return new Vault(token);
}
