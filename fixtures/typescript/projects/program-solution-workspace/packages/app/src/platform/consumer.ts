// Single specifier "./service" resolves to different files under moduleSuffixes context.
// Ordered suffixes [".ios",".native",""] — .ios preferred, then .native, then empty.
import { describeService } from "./service.js";

export function consumePlatform(): string {
  return describeService();
}
