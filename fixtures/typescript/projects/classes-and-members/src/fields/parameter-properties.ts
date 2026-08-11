// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Constructor parameter properties: public, protected, private, readonly.
 * Destructuring does NOT create a parameter property; explicit property is required.
 */
export class ParameterProperties {
  constructor(
    public publicTag: string,
    protected protectedCount: number,
    private privateFlag: boolean,
    readonly readonlyId: string,
    public optionalPublic?: string,
  ) {}

  getPrivateFlag(): boolean {
    return this.privateFlag;
  }

  getProtectedCount(): number {
    return this.protectedCount;
  }
}

/** Derived constructor injection around super. */
export class DerivedParameterProperties extends ParameterProperties {
  constructor(
    public derivedLabel: string,
    publicTag: string,
    protectedCount: number,
    privateFlag: boolean,
    readonlyId: string,
  ) {
    super(publicTag, protectedCount, privateFlag, readonlyId);
    // Initialization after super; reading base field here would observe defined value.
    void this.derivedLabel;
  }
}

/** Destructuring in constructor is not a parameter property; manual assignment needed. */
export class DestructuredParam {
  host: string;
  port: number;

  constructor({ host, port }: { host: string; port: number }) {
    this.host = host;
    this.port = port;
  }
}

export function exerciseParameterProperties(): void {
  const p = new ParameterProperties("pub", 42, true, "id-1");
  void p.publicTag;
  void p.getPrivateFlag();
  void new DerivedParameterProperties("derived", "pub", 1, false, "id-2");
  void new DestructuredParam({ host: "localhost", port: 8080 });
}
