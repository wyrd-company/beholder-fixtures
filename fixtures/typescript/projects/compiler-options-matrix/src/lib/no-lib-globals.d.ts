// Fixture-owned minimal global declarations for noLib context.
// With noLib true the bundled default library is not loaded; this file supplies
// the core global types needed to keep the program valid.

interface Array<T> {
  length: number;
  push(item: T): number;
  at(index: number): T | undefined;
}

interface Boolean {}
interface CallableFunction {}
interface Function {}
interface IArguments {}
interface NewableFunction {}
interface Number {}
interface Object {}
interface RegExp {}
interface String {
  length: number;
  charAt(pos: number): string;
}

declare const console: {
  log(...args: unknown[]): void;
};
