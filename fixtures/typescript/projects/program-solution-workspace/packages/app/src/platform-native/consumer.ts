// Same specifier "./service" under moduleSuffixes [".ios",".native",""].
// No .ios file present in this directory, so .native is selected.
import { describeService } from "./service.js";

export function consumePlatformNative(): string {
  return describeService();
}
