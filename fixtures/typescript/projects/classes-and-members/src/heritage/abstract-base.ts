// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface Auditable {
  audit(): string;
}

export interface Serializable {
  serialize(): string;
}

/** Abstract base exercising abstract members, protected/private visibility, and override checking. */
export abstract class Shape {
  protected tag: string;

  protected constructor(tag: string) {
    this.tag = tag;
  }

  abstract area(): number;

  describe(): string {
    return `shape:${this.tag}`;
  }

  /** Protected member for assignability checks. */
  protected revision(): string {
    return "rev-1";
  }

  // Private member participates in compatibility checks but is not accessible to subclasses.
  private brand = "shape-brand";
  protected getBrand(): string {
    return this.brand;
  }
}
