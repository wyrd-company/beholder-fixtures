export interface Edge {
  from: string;
  to: string;
  weight: number;
}

export type GraphEdges = Edge[];

export function edgeLabel(e: Edge): string {
  return `${e.from}->${e.to}:${e.weight}`;
}
