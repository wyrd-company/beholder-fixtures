// Excluded file re-entering through import — excluded by config but imported here.
import { excludedValue } from "../excluded/should-be-excluded.js";

export function consumeExcluded(): string {
  return `via-import:${excludedValue}`;
}
