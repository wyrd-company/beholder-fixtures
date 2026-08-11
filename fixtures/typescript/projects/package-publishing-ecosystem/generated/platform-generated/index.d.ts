// Generated typed platform module — condition-selected browser/server/native via generated source.

export interface PlatformGeneratedMarker {
  source: "generated-platform";
  platform: "browser" | "server" | "native";
  env: "development" | "production";
}

export declare function describeGeneratedPlatform(
  platform: PlatformGeneratedMarker["platform"],
): string;
