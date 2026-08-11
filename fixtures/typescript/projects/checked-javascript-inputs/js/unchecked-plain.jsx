/**
 * Plain unchecked JSX — no file directive; checked via project `checkJs`.
 */

/**
 * @param {{ text: string }} props
 */
function Plain(props) {
  return <span>{props.text}</span>;
}

module.exports = { Plain };
