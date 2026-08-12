export { coreTag, formatLabel } from "./core/index.js";
export { makeLeaf, joinIds } from "./core/util.js";
export { runExplicit } from "./core/consumer-explicit.js";
// runDirectory is provided via directory import in src/directory-consumer.ts (bundler context)
export { runViaImportsField } from "./core/exports-consumer.js";
export { readA, linkAtoB } from "./graph/node-a.js";
export { readB, linkBtoA } from "./graph/node-b.js";
export { ready, getReady } from "./graph/top-level-await.js";
export { metaUrl, describeMeta } from "./graph/import-meta.js";
export { preserved } from "./graph/preserve-consumer.js";
export { Panel } from "./formats/component.jsx";
export { describeNative } from "./formats/native.mjs";
export { describeLegacy } from "./formats/legacy.cjs";
export { describeMixed } from "./formats/mixed.js";
export { viaJsExtension } from "./formats/ts-via-js.js";
export { bridgeFormats } from "./formats/extension-bridge.js";
export { checkNearestType } from "./formats/nearest-type-check.js";
export { viaReal } from "./identity/alias-via-real.js";
export { viaLink } from "./identity/alias-via-link.js";
export {
  checkUnify,
  checkTwoVersions,
} from "./identity/dual-identity-consumer.js";
export { checkSpellings } from "./identity/symlink-spellings.js";
export { consumeExports } from "./exports/exports-consumer.js";
export { consumeJsCompat } from "./js-compat/consumer.js";
