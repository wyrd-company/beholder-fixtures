// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Static private fields with instance and static sides. */
export class Registry {
  private static _entries: string[] = [];
  static #token = "registry-token";

  static register(entry: string): void {
    this._entries.push(entry);
    void this.#token;
  }

  static entries(): string[] {
    return [...this._entries];
  }

  static getToken(): string {
    return this.#token;
  }

  /** Instance private static interaction. */
  static describeStaticState(): string {
    return `${this.#token}:${this._entries.length}`;
  }
}

export class CounterWithStaticPrivate {
  static #count = 0;
  #instanceId = ++CounterWithStaticPrivate.#count;

  getId(): number {
    return this.#instanceId;
  }
  static total(): number {
    return CounterWithStaticPrivate.#count;
  }
}

export function exerciseStaticPrivate(): void {
  Registry.register("a");
  void Registry.entries();
  void Registry.getToken();
  const c = new CounterWithStaticPrivate();
  void c.getId();
  void CounterWithStaticPrivate.total();
}
