using System.Reflection;
using System.Runtime.CompilerServices;
using Fixture.AttributesAndMetadata.Core.Attributes;
using Fixture.AttributesAndMetadata.ReferencedModule;

[module: Showcase("module-target")]

[assembly: Showcase("assembly-target")]
[assembly: Showcase("assembly-target-secondary")]
[assembly: AssemblyMetadata("FixtureProject", "attributes-and-metadata")]

namespace Fixture.AttributesAndMetadata.Core;

/// <summary>
/// Declares several module initializers for this assembly's own module and
/// exposes their combined effect without asserting which one ran first; the
/// contract only guarantees all module initializers run once, before any
/// other code in the module, not a relative order among themselves.
/// </summary>
internal static class ModuleInitialization
{
    internal static bool PrimaryRan { get; private set; }

    internal static bool SecondaryRan { get; private set; }

    internal static int RunCount { get; private set; }

    [ModuleInitializer]
    internal static void InitializePrimary()
    {
        PrimaryRan = true;
        RunCount++;
    }

    [ModuleInitializer]
    internal static void InitializeSecondary()
    {
        SecondaryRan = true;
        RunCount++;
    }
}

/// <summary>
/// Observes the combined state left by <see cref="ModuleInitialization"/> and
/// by the module initializer declared in the referenced
/// <c>ReferencedModule</c> assembly, ahead of any other ordinary use of
/// either module.
/// </summary>
public static class ModuleInitializationObservation
{
    public static string Describe()
    {
        var referencedModuleRan = ReferencedModuleInitialization.Ran;
        return $"core-primary={ModuleInitialization.PrimaryRan} " +
               $"core-secondary={ModuleInitialization.SecondaryRan} " +
               $"core-run-count={ModuleInitialization.RunCount} " +
               $"referenced-module={referencedModuleRan}";
    }
}
