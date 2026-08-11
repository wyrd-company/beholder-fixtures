// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Static fields, methods, private state, blocks, inheritance, and block order. */

const initLog: string[] = [];

export class StaticBase {
  static baseTag = "base";
  static describeBase(): string {
    return this.baseTag;
  }

  static #privateBase = "private-base";
  static getPrivateBase(): string {
    return this.#privateBase;
  }

  static {
    initLog.push("StaticBase:block-1");
  }

  static {
    initLog.push("StaticBase:block-2");
  }
}

export class StaticDerived extends StaticBase {
  static derivedTag = "derived";

  static override describeBase(): string {
    // static inheritance: `this` is the derived constructor; super dispatch
    const base = super.describeBase();
    return `${base}->${this.derivedTag}:${this.derivedTag}`;
  }

  static getBasePrivate(): string {
    // Derived cannot access #privateBase directly; uses base accessor
    return StaticBase.getPrivateBase();
  }

  static thisHost(this: typeof StaticDerived): string {
    return this.derivedTag;
  }

  static {
    initLog.push("StaticDerived:block-1");
  }

  static {
    initLog.push("StaticDerived:block-2");
  }
}

export function getInitLog(): string[] {
  return [...initLog];
}

export class WithStaticState {
  static count = 0;
  static #token = "with-token";

  static increment(): void {
    this.count += 1;
  }

  static getToken(): string {
    return this.#token;
  }

  static describe(): string {
    return `${this.count}:${this.#token}`;
  }
}

export function exerciseStaticMembers(): void {
  void StaticBase.baseTag;
  void StaticDerived.derivedTag;
  void StaticDerived.describeBase();
  void StaticDerived.thisHost();
  void WithStaticState.describe();
  void getInitLog();
}
