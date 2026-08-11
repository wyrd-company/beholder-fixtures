// @ts-nocheck

/**
 * Unchecked JSX — type checking suppressed by `// @ts-nocheck` even though
 * project `checkJs` is on. Contrast with checked `component.jsx`.
 */

/**
 * @param {{ text: string }} props
 */
function View(props) {
  return <span>{props.text}</span>;
}

module.exports = { View };
