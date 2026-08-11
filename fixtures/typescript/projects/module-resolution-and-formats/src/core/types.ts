export type NodeKind = "leaf" | "branch";

export interface GraphNode {
  kind: NodeKind;
  id: string;
  next?: GraphNode;
}

export interface ResolverResult {
  path: string;
  format: "esm" | "cjs";
}

export function describeNode(node: GraphNode): string {
  return `${node.kind}:${node.id}`;
}
