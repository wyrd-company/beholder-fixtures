export interface NativeDecl {
  kind: "native-mts";
  token: string;
}

export declare function readNativeDecl(decl: NativeDecl): string;
