export interface AliasMarker {
  source: "built";
  value: string;
}
export declare function readAlias(value: string): AliasMarker;
