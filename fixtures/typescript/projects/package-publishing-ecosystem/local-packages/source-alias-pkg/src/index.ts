export interface AliasMarker {
  source: "src-alias";
  value: string;
}

export function readAlias(value: string): AliasMarker {
  return { source: "src-alias", value };
}
