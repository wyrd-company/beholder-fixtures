// Same specifier "./service" — only empty suffix file exists, so fallback selected.
import { describeService } from "./service.js";

export function consumePlatformEmpty(): string {
  return describeService();
}
