// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { Shape, Auditable, Serializable } from "./abstract-base.js";

/** Concrete derived class implementing multiple interfaces and overriding correctly. */
export class Rectangle extends Shape implements Auditable, Serializable {
  constructor(
    tag: string,
    public width: number,
    public height: number,
  ) {
    super(tag);
  }

  override area(): number {
    return this.width * this.height;
  }

  override describe(): string {
    // super dispatch
    const base = super.describe();
    const rev = super.revision();
    return `${base}:${this.width}x${this.height}:${rev}`;
  }

  audit(): string {
    return `audit:${this.tag}`;
  }

  serialize(): string {
    return JSON.stringify({ tag: this.tag, w: this.width, h: this.height });
  }

  /** Exposes protected access from subclass. */
  getRevision(): string {
    return this.revision();
  }
}

/** Demonstrate protected and private assignability. */
export function exerciseAssignability(): void {
  const rect = new Rectangle("r1", 3, 4);
  const shape: Shape = rect; // protected/private compatibility checked via assignability
  void shape.describe();
  void rect.getRevision();
  // Hard private brand is not accessible here; compatibility remains structural elsewhere.
}
