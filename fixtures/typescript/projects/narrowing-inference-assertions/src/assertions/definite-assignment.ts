// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class LedgerContainer {
  declare revision: string;
  label!: string;
  count!: number;

  initialize(label: string, count: number): void {
    this.label = label;
    this.count = count;
  }

  read(): string {
    return `${this.label}:${this.count}`;
  }
}

export class AtlasHolder {
  definiteLabel!: string;
  definiteCount!: number;
  optionalNote?: string;

  constructor(label: string, count: number) {
    this.definiteLabel = label;
    this.definiteCount = count;
  }

  describe(): string {
    return `${this.definiteLabel}:${this.definiteCount}`;
  }
}

export function lifecycleInitializedField(): string {
  const holder = new LedgerContainer();
  holder.initialize("atlas", 3);
  return holder.read();
}

export let deferredLabel!: string;

export function initializeDeferred(): void {
  deferredLabel = "atlas";
}

export function readDeferred(): string {
  return deferredLabel.toUpperCase();
}
