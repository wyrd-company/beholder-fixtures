export declare function read(value: string): string;
export declare const marker: "workspace";
export declare function workspaceOnly(value: string): string;
export type CustomDepWorkspace = { kind: "workspace"; extra: string };
export type CustomDepDefault = { kind: "workspace"; extra: string };
