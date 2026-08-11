function read(value) {
  return `workspace-cjs:${value}`;
}
function workspaceOnly(value) {
  return `workspace-only-cjs:${value}`;
}
module.exports = { read, marker: "workspace", workspaceOnly };
