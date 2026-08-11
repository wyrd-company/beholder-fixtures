// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// JavaScript constructor function with prototype, demonstrating constructor functions in JavaScript
// and dynamic this on prototype methods. This file is checked via allowJs / checkJs in tsconfig.

/**
 * @param {string} name
 */
export function JsBox(name) {
  /** @type {string} */
  this.name = name;
}

JsBox.prototype.describe = function () {
  return this.name;
};

JsBox.prototype.describeArrow = function () {
  const arrow = () => this.name;
  return arrow();
};
