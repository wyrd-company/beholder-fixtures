using System.Diagnostics.CodeAnalysis;

namespace Acme.Deployment.Trimming;

public static class FeatureSwitches
{
    // Feature switch: the linker substitutes the return value at publish time.
    // The [FeatureSwitchDefinition] marks the switch name for the trimmer.
    public const string DiagnosticsSwitch = "Acme.Deployment.EnableDiagnostics";

    [FeatureSwitchDefinition(DiagnosticsSwitch)]
    public static bool IsDiagnosticsEnabled => AppContext.TryGetSwitch(DiagnosticsSwitch, out var enabled) && enabled;

    public static string DescribeSwitch()
    {
        if (IsDiagnosticsEnabled)
        {
            return "diagnostics-enabled";
        }

        return "diagnostics-disabled";
    }

    // RequiresUnreferencedCode guarded by feature switch — trimmer can remove branch.
    [RequiresUnreferencedCode("Diagnostics path uses reflection.")]
    public static string DiagnosticsReflectionPath()
    {
        var t = Type.GetType("Acme.Deployment.Trimming.TrimSample, Trimming");
        return t?.FullName ?? "no-type";
    }

    public static string ConditionalDiagnostics()
    {
        if (IsDiagnosticsEnabled)
        {
            // Warning if caller does not propagate RequiresUnreferencedCode.
            return DiagnosticsReflectionPath();
        }

        return "skipped";
    }

    [RequiresUnreferencedCode("Propagates conditional reflection.")]
    public static string ConditionalDiagnosticsPropagated()
    {
        if (IsDiagnosticsEnabled)
        {
            return DiagnosticsReflectionPath();
        }

        return "skipped-propagated";
    }
}
