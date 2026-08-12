// alwaysStrict: script-form source to observe emit difference.
// This file has no imports or exports, so it is a script. With alwaysStrict true
// the emitted JavaScript contains a "use strict" prologue; with false it does not.

function computeStrict(value: number): number {
  return value * 2;
}

var legacyCounter = 0;

function incrementCounter(): number {
  legacyCounter += 1;
  return legacyCounter;
}
