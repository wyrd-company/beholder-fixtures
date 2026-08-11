using System.Runtime.CompilerServices;

namespace Fixture.AttributesAndMetadata.ReferencedModule;

/// <summary>
/// Owns a module initializer that lives in an assembly referenced by
/// <c>Core</c>, distinct from the module initializers <c>Core</c> declares
/// for itself.
/// </summary>
public static class ReferencedModuleInitialization
{
    public static bool Ran { get; private set; }

    [ModuleInitializer]
    public static void Initialize() => Ran = true;
}
