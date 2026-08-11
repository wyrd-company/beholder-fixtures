using System.Runtime.CompilerServices;

namespace Fixture.AttributesAndMetadata.Contexts.CSharp9
{
    /// <summary>Module initializers became valid at their C# 9 version floor; built here under <c>LangVersion 9.0</c>.</summary>
    internal static class ModuleInitializerBoundary
    {
        internal static bool Ran { get; private set; }

        [ModuleInitializer]
        internal static void Initialize() => Ran = true;
    }

    public static class ModuleInitializerBoundaryObservation
    {
        public static string Describe() => $"module-initializer-at-langversion-9-declared initial-flag={ModuleInitializerBoundary.Ran}";
    }
}
