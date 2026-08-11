using System.Reflection;

// The SDK's generated assembly-info targets have no MSBuild property for assembly
// culture, so the distinct, non-neutral culture dimension of assembly identity is
// declared directly via the attribute.
[assembly: AssemblyCulture("en-GB")]

namespace Acme.Identity;

public sealed class SharedWidget
{
    public string Origin => "Identity.CulturedLibrary v1.0.0 (en-GB)";
    public static string AssemblyName => typeof(SharedWidget).Assembly.GetName().Name!;
    public static string Culture => typeof(SharedWidget).Assembly.GetName().CultureName!;
    public string Describe() => $"Widget from {AssemblyName} v{typeof(SharedWidget).Assembly.GetName().Version} culture={Culture}";
}
