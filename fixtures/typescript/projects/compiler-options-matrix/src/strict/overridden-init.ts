// Child override for strictPropertyInitialization: valid only when the flag is false.
// Under strict true, label must be initialized or asserted; under overridden false it may remain uninitialized.

export class UninitializedLabel {
  label: string;

  constructor() {
    // No assignment; allowed only when strictPropertyInitialization is false.
  }

  setLabel(value: string): void {
    this.label = value;
  }
}
