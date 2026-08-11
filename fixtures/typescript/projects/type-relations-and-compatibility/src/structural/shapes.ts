export interface Coordinate {
  x: number;
  y: number;
}

export interface CoordinateTwin {
  x: number;
  y: number;
}

export function assignIndependentShapes(): Coordinate {
  const twin: CoordinateTwin = { x: 1, y: 2 };
  const point: Coordinate = twin;
  return point;
}

export interface WeakPreferences {
  theme?: string;
  density?: number;
}

export function acceptWeakTarget(candidate: WeakPreferences): WeakPreferences {
  return candidate;
}

export type UserId = string & { readonly __brand: unique symbol };

export function brandUserId(raw: string): UserId {
  return raw as UserId;
}

export function useBrandedId(id: UserId): UserId {
  return id;
}

export interface TreeNode {
  label: string;
  children?: TreeNode[];
}

export function buildTree(): TreeNode {
  const leaf: TreeNode = { label: "leaf" };
  const branch: TreeNode = { label: "branch", children: [leaf] };
  return branch;
}

export interface OptionalNote {
  title: string;
  subtitle?: string;
}

export function optionalMember(note: OptionalNote): string | undefined {
  return note.subtitle;
}
