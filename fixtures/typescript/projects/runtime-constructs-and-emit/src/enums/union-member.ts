// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export enum UnionKind {
  Alpha = "ALPHA",
  Beta = "BETA",
  Gamma = "GAMMA",
}

export type UnionMember = UnionKind.Alpha | UnionKind.Beta;

export function isUnionMember(value: UnionKind): value is UnionMember {
  return value === UnionKind.Alpha || value === UnionKind.Beta;
}

export function describeUnionMember(value: UnionMember): string {
  return `union:${value}`;
}

export function consumeUnionKind(value: UnionKind): string {
  if (isUnionMember(value)) {
    return describeUnionMember(value);
  }
  return `other:${value}`;
}
