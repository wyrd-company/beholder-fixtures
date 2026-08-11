declare module "fs" {
  export function readFileSync(path: string, encoding?: string): string;
  export function existsSync(path: string): boolean;
}
declare module "node:fs" {
  export function readFileSync(path: string, encoding?: string): string;
}
declare const process: { exit(code: number): never };
