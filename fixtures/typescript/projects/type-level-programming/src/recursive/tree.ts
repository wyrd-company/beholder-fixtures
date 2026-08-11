// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-074: recursive interface/tree, recursive tuple/object alias, mutually recursive aliases,
// conditional/mapped recursion, circular property reference, serialization-shaped cycle

// Recursive interface / tree
export interface TreeNode {
  label: string;
  children: TreeNode[];
}

export const treeExample: TreeNode = {
  label: "atlas",
  children: [{ label: "beacon", children: [] }],
};

// Recursive tuple alias
export type NestedTuple = [string, NestedTuple | null];

export const nestedTupleExample: NestedTuple = ["atlas", ["ledger", null]];

// Recursive object alias
export type LinkedEntry = {
  value: string;
  next: LinkedEntry | null;
};

export const linkedExample: LinkedEntry = {
  value: "atlas",
  next: { value: "ledger", next: null },
};

// Mutually recursive aliases
export type HarborEntry = {
  tag: "harbor";
  next: RecursiveOrchardEntry | null;
};

export type RecursiveOrchardEntry = {
  tag: "orchard";
  next: HarborEntry | null;
};

export const mutualExample: HarborEntry = {
  tag: "harbor",
  next: { tag: "orchard", next: null },
};

// Circular property reference (self-referential via property)
export type CircularRef = {
  label: string;
  self: CircularRef;
};

export function getCircularLabel(node: CircularRef): string {
  return node.self.label;
}

// Serialization-shaped cycle (JSON-like)
export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

export const jsonExample: JsonValue = {
  label: "atlas",
  count: 3,
  nested: ["beacon", { tag: "harbor" }],
};

// Alias versus interface presentation: same shape, different declaration kind
export interface InterfaceTree {
  label: string;
  children: InterfaceTree[];
}

export type AliasTree = {
  label: string;
  children: AliasTree[];
};

export const interfaceTree: InterfaceTree = { label: "atlas", children: [] };
export const aliasTree: AliasTree = { label: "atlas", children: [] };
