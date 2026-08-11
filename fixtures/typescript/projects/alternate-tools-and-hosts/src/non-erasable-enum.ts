/**
 * Non-erasable syntax: enum is runtime-visible and cannot be stripped.
 * Node.js --experimental-strip-types rejects this file; Bun succeeds (TS-CAN-091).
 * Also the construct whose transform differs between tsc and Bun (TS-CAN-090).
 */

export enum Status {
  Pending = 0,
  Active = 1,
  Done = 2,
}

export const current: Status = Status.Active;

export function isActive(s: Status): boolean {
  return s === Status.Active;
}
