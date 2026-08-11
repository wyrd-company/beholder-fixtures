/**
 * Erasable syntax: every construct here can be stripped by type-only erasure.
 * Node.js --experimental-strip-types succeeds on this file (TS-CAN-091).
 */

export type Alias = string;

export interface Item {
  id: number;
  name: string;
}

export type Handler<T> = (value: T) => void;

export type Config = {
  debug: boolean;
  label?: string;
};

export function makeItem(id: number, name: string): Item {
  return { id, name };
}

export const handleItem: Handler<Item> = (value) => {
  void value;
};

export const defaultConfig: Config = { debug: false };
