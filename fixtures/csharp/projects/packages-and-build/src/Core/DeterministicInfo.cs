// CS-CAN-105: deterministic, path-mapped, portable PDB, embedded source.
// Build is deterministic (Deterministic=true, DeterministicSourcePaths=true, PathMap=/repo/packages-and-build/),
// debug type portable, embedded sources, and Source Link readiness via PublishRepositoryUrl.
// Caller path is path-mapped; sequence points are in portable PDB; source is embedded.
using System.Runtime.CompilerServices;

namespace Catalog.Packages;

public static class DeterministicInfo
{
    // #line demonstrates caller path mapping and sequence points; PathMap rewrites absolute repo paths.
#line 42 "/repo/packages-and-build/src/Core/DeterministicInfo.cs"
    public static string CallerFile([CallerFilePath] string path = "") => path;

    public static string CallerMember([CallerMemberName] string member = "") => member;

    // Physical vs mapped path observation: caller file path is the mapped deterministic path.
    public static bool IsMappedPath(string path) => path.StartsWith("/repo/packages-and-build/");

    public static string BuildId => "deterministic-v1";
}
