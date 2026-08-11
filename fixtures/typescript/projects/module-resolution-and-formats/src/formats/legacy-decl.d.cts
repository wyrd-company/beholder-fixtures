export interface LegacyDecl {
  kind: "legacy-cts";
  marker: string;
}

export declare function readLegacyDecl(decl: LegacyDecl): string;
