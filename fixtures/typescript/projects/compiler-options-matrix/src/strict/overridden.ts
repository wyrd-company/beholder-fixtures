// Child option overriding strict: true.
// This file is compiled with strict true but strictNullChecks and strictPropertyInitialization overridden to false.
// The same source shows that a child flag can relax the umbrella while keeping other strict checks.

export interface OverriddenShape {
  id: string;
  note: string | null;
}

export function readOverriddenNote(shape: OverriddenShape): string {
  // Under strictNullChecks true this requires explicit null handling;
  // under overridden false the null collapse still requires handling for validity,
  // but the type is relaxed and assignment to string becomes permissive.
  return shape.note ?? "default-note";
}

export class OverriddenInit {
  // With strictPropertyInitialization overridden off, this field need not be
  // definitely assigned in the constructor for the overridden context.
  // Under strict true alone it would require initialization or assertion.
  label: string = "initial";

  constructor(label?: string) {
    if (label) {
      this.label = label;
    }
  }
}
