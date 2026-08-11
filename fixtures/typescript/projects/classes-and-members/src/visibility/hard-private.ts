// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Hard #private fields, methods, narrowing, and static private. */
export class Vault {
  #secret = "vault-secret";
  #counter = 0;

  static #instanceCount = 0;
  static #register(): void {
    Vault.#instanceCount += 1;
  }

  constructor() {
    Vault.#register();
  }

  revealSecret(): string {
    return this.#secret;
  }

  increment(): void {
    this.#counter += 1;
  }

  /** `#x in obj` narrowing for hard private brand check. */
  owns(obj: unknown): obj is Vault {
    return #secret in (obj as Vault) && #counter in (obj as Vault);
  }

  /** Runtime brand check function. */
  static isVault(obj: unknown): obj is Vault {
    return obj instanceof Vault && #secret in obj;
  }

  static getInstanceCount(): number {
    return Vault.#instanceCount;
  }

  /** Hard private method. */
  #hash(): string {
    return `${this.#secret}:${this.#counter}`;
  }

  getHash(): string {
    return this.#hash();
  }
}

export function exerciseHardPrivate(): void {
  const v = new Vault();
  void v.revealSecret();
  v.increment();
  void v.getHash();
  void Vault.getInstanceCount();
  void Vault.isVault(v);
  void Vault.isVault({});

  const maybeVault: unknown = v;
  if (v.owns(maybeVault)) {
    void maybeVault.revealSecret();
  }
}
