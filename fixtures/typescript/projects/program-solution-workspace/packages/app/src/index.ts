import type { RelayPayload } from "../../core/src/index.js";
import { computeResult, formatResult } from "../../core/src/index.js";
import { describeAlias } from "./alias/alias-consumer.js";
import { consumePlatform } from "./platform/consumer.js";
import { readWildcard } from "./wildcard/wildcard-consumer.js";
import { describeRootDirs } from "./rootdirs/shared.js";
import { readCrossRoot } from "./cross-root-consumer.js";
import type { GeneratedModel } from "../../../generated/models.js";
import { readGeneratedApi } from "../../../generated/api.js";

export type AppPayload = RelayPayload & { source: string };

export function runApp(payload: AppPayload): string {
  const result = computeResult(payload);
  const label = formatResult(result);
  const alias = describeAlias(payload.id);
  const platform = consumePlatform();
  const wildcard = readWildcard();
  const rootDirs = describeRootDirs();
  const cross = readCrossRoot();
  const generated: GeneratedModel = { id: payload.id, revision: 1 };
  return [
    label,
    alias,
    platform,
    wildcard,
    rootDirs,
    cross,
    readGeneratedApi(generated),
  ].join("|");
}

// Re-export public declaration consumption across composite boundary.
export type { RelayResult } from "../../core/src/index.js";
