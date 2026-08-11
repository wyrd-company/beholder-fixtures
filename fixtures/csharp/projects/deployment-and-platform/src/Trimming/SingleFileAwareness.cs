using System.Diagnostics.CodeAnalysis;
using System.Reflection;

namespace Acme.Deployment.Trimming;

public static class SingleFileAwareness
{
    // Assembly.Location changes under single-file publish (empty or bundle path).
    public static string DescribeAssemblyLocation()
    {
        var location = Assembly.GetExecutingAssembly().Location;
        return string.IsNullOrEmpty(location) ? "single-file-or-trimmed" : location;
    }

    // AppContext.BaseDirectory remains stable under single-file.
    public static string DescribeBaseDirectory() => AppContext.BaseDirectory;

    // Single-file analyzer: code that probes the file system near the assembly.
    [RequiresAssemblyFiles("Assembly file may not be present in single-file.")]
    public static string ReadAssemblyFile()
    {
        var path = Assembly.GetExecutingAssembly().Location;
        return File.Exists(path) ? File.ReadAllText(path).Length.ToString() : "no-file";
    }

    public static void TriggerSingleFileWarning()
    {
        // IL3002: calling RequiresAssemblyFiles without annotation warns.
        _ = ReadAssemblyFile();
    }

    [RequiresAssemblyFiles("Propagates single-file requirement.")]
    public static void PropagatedSingleFileCaller()
    {
        _ = ReadAssemblyFile();
    }

    // Environment.ProcessPath vs Assembly.Location distinction.
    public static string DescribeProcessPath() => Environment.ProcessPath ?? "no-process-path";
}
