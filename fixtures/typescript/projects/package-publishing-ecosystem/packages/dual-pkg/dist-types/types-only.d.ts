export interface TypesOnlyMarker {
  kind: "types-only";
  value: string;
}
export type DescribeTypesOnly = (value: TypesOnlyMarker) => string;
