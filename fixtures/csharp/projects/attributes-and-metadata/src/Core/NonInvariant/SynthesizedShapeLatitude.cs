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
}
