// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const atlasRuntimeView = (
  <>
    <atlas-panel label="atlas-runtime" priority={5} />
    <catalog:item catalog="atlas" code="runtime-surface" />
    <ns:widget ns:priority="atlas" catalog:kind="atlas" />
  </>
);
