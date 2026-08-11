// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function narrowWithAssertion(token: string): string {
  const narrowed = <string>token;
  return narrowed;
}

export const commaDisambiguatedMapper = <T>(value: T): T => value;

export function selectMapper<T, U>(mapper: <V>(item: V) => V): typeof mapper {
  return mapper;
}

export function buildMapperPair<T>() {
  const identity = <U>(item: U): U => item;
  return { identity, commaDisambiguatedMapper };
}
