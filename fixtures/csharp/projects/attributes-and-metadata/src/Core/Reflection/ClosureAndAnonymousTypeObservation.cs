using System.Runtime.CompilerServices;

namespace Fixture.AttributesAndMetadata.Core.Reflection;

public static class ClosureHost
{
    public static Func<int> MakeCounter(int seed)
    {
        var state = seed;
        return () => ++state;
    }
}

/// <summary>
/// Reflects over a lambda's compiler-generated closure and over an anonymous
/// type, both identified only by <see cref="CompilerGeneratedAttribute"/>
/// and structural shape, never by synthesized names, per CS-CAN-125.
/// </summary>
public static class ClosureAndAnonymousTypeObservation
{
    public static string DescribeClosure()
    {
        var counter = ClosureHost.MakeCounter(10);
        var isCompilerGenerated = counter.Method.IsDefined(typeof(CompilerGeneratedAttribute), false);
        var targetIsCompilerGenerated = counter.Target?.GetType().IsDefined(typeof(CompilerGeneratedAttribute), false) ?? false;

        return $"closure-method-compiler-generated={isCompilerGenerated} closure-target-compiler-generated={targetIsCompilerGenerated}";
    }

    public static string DescribeAnonymousType()
    {
        var sample = new { Label = "anonymous", Value = 7 };
        var type = sample.GetType();

        return $"anonymous-type-compiler-generated={type.IsDefined(typeof(CompilerGeneratedAttribute), false)} " +
               $"property-count={type.GetProperties().Length}";
    }
}
