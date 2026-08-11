// CS-CAN-099: language-version and compiler-version selection.
// Records the single installed compiler and SDK version; language-version gating is demonstrated by the separate LangVersion* projects.
// This file is the version record for the default context.
namespace Catalog.Packages;

public static class CompilerVersion
{
    public const string SdkVersion = "10.0.110";
    public const string CompilerVersionString = "4.14.0"; // Roslyn bundled with SDK 10.0.110
    public const string RuntimeVersion = "10.0.10";
    public const string TargetFrameworkDefault = "net10.0";
    public const string LanguageVersionDefault = "latest"; // SDK default for net10.0
}
