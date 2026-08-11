// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export interface RecordShape {
  id: string;
}

export interface Sized {
  width: number;
  height: number;
}

export interface Labeled {
  label: string;
}
