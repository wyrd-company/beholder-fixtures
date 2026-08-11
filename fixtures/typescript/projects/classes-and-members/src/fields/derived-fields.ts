// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { BaseFields } from "./base-fields.js";

/**
 * Derived class demonstrating:
 * - initialized vs uninitialized fields
 * - field shadowing a base setter (define vs assignment semantics)
 * - initialization order around super
 * - useDefineForClassFields emit difference (observed in dist vs dist-downlevel)
 */
export class DerivedFields extends BaseFields {
  /** Initialized field in derived. */
  derivedInitialized = "derived-init";

  /** Uninitialized field. */
  derivedUninitialized!: number;

  /**
   * Field shadowing base setter `shadowed`.
   * Under `useDefineForClassFields: true` this defines an own data property, shadowing the accessor.
   * Under `false` it assigns via `this.shadowed = ...` invoking the setter.
   * TypeScript 4.3+ reports TS2610 for accessor/property override; suppression is intentional
   * to preserve the valid runtime emit difference that the fixture must demonstrate.
   */
  // @ts-ignore: TS2610 — intentional field shadowing accessor to show define vs assignment emit
  override shadowed = "derived-shadowing-field";

  declare derivedDeclared: string;

  constructor(label: string) {
    // Accessing `this` before super is not allowed; initialization happens after super.
    super();
    this.derivedUninitialized = label.length;
    // Reading a field after super is valid.
    void this.initialized;
    void this.shadowed;
  }
}

export function exerciseFields(): void {
  const d = new DerivedFields("hello");
  void d.derivedInitialized;
  void d.derivedUninitialized;
  void d.shadowed;
}
