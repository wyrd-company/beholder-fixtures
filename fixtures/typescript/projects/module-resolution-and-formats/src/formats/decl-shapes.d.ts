export interface DeclShape {
  tag: string;
  value: number;
}

export declare function readShape(shape: DeclShape): string;

export type DeclAlias = DeclShape;
