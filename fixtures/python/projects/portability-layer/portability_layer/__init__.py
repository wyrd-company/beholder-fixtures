"""Portability layer over filesystem, locale, time and process APIs."""

from portability_layer.build_info import BuildInfo, collect_build_info
from portability_layer.clocks import AmbiguousWallTime, ClockComparison, TimestampPrecision
from portability_layer.environment import StartupProbe, spawn_isolated, spawn_with_env
from portability_layer.filesystem import PathKind, normalize_text_path, resolve_portable_path
from portability_layer.hashing import HashSeedMode, deterministic_hash_report, sorted_serialization
from portability_layer.path_identity import PathIdentity, compare_paths
from portability_layer.platform_api import PlatformSupport, UnsupportedPlatformError, get_platform_helper
from portability_layer.processes import ProcessResult, run_bytes_mode, run_text_mode, run_with_argv
from portability_layer.text_encoding import EncodingResult, read_with_explicit_utf8, read_with_universal_newlines

__all__ = [
    "AmbiguousWallTime",
    "BuildInfo",
    "ClockComparison",
    "EncodingResult",
    "HashSeedMode",
    "PathIdentity",
    "PathKind",
    "PlatformSupport",
    "ProcessResult",
    "StartupProbe",
    "TimestampPrecision",
    "UnsupportedPlatformError",
    "collect_build_info",
    "compare_paths",
    "deterministic_hash_report",
    "get_platform_helper",
    "normalize_text_path",
    "read_with_explicit_utf8",
    "read_with_universal_newlines",
    "resolve_portable_path",
    "run_bytes_mode",
    "run_text_mode",
    "run_with_argv",
    "sorted_serialization",
    "spawn_isolated",
    "spawn_with_env",
]
