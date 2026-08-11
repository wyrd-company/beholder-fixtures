using System.Reflection;
using System.Runtime.CompilerServices;
using Fixture.AttributesAndMetadata.Core.Attributes;

namespace Fixture.AttributesAndMetadata.Core.NonInvariant;

/// <summary>
/// CS-CAN-125: observes synthesized shapes (a record's compiler-generated
/// members, a capturing lambda's compiler-generated closure target) only
/// through semantic association — presence and marker attributes — never
/// through an exact private name, member count, or declaration order, all of
/// which Roslyn is free to vary across versions and optimization levels.
/// </summary>
public static class SynthesizedShapeLatitude
{
    public static string DescribeRecordSynthesizedMembers()
    {
        var hasCompilerGeneratedMethod = typeof(ShowcaseRecord)
            .GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
            .Any(m => m.IsDefined(typeof(CompilerGeneratedAttribute), false));

        return $"record-has-compiler-generated-member={hasCompilerGeneratedMethod}";
    }

    public static string DescribeLambdaShape()
    {
        var captured = 3;
        Func<int, int> lambda = x => x + captured;

        // Roslyn marks the capturing lambda's closure target (its display
        // class instance), not necessarily the invoked method itself, so the
        // target's type is the reliable place to look for the marker.
        var targetIsCompilerGenerated = lambda.Target?.GetType().IsDefined(typeof(CompilerGeneratedAttribute), false) ?? false;

        return $"lambda-closure-target-compiler-generated={targetIsCompilerGenerated}";
    }

    public static string DescribeLocalFunctionSynthesis()
    {
        var capturingResult = LocalFunctionHost.InvokeCapturingLocalFunction(3);
        var staticResult = LocalFunctionHost.InvokeStaticLocalFunction(4);

        // A capturing local function is lowered onto a compiler-generated
        // closure type or method; a non-capturing (static) local function is
        // ordinarily an unmarked private method. Presence is checked across
        // both nested types and declared methods, never by a specific name.
        var hasCompilerGeneratedArtifact =
            typeof(LocalFunctionHost).GetNestedTypes(BindingFlags.NonPublic)
                .Any(t => t.IsDefined(typeof(CompilerGeneratedAttribute), false))
            || typeof(LocalFunctionHost).GetMethods(BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.DeclaredOnly)
                .Any(m => m.IsDefined(typeof(CompilerGeneratedAttribute), false));

        return $"capturing-local-function-result={capturingResult} static-local-function-result={staticResult} " +
               $"local-function-compiler-generated-artifact-present={hasCompilerGeneratedArtifact}";
    }
}

public static class LocalFunctionHost
{
    public static int InvokeCapturingLocalFunction(int seed)
    {
        int Compute(int x) => (x * 2) + seed;
        return Compute(seed);
    }

    public static int InvokeStaticLocalFunction(int value)
    {
        static int Double(int x) => x * 2;
        return Double(value);
    }
}
