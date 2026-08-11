using System.Diagnostics.CodeAnalysis;

namespace Acme.Deployment.Trimming;

public static class AotCompatibility
{
    [RequiresDynamicCode("MakeGenericType is not AOT compatible.")]
    public static object CreateGenericViaReflection(Type genericDefinition, Type argument)
    {
        var constructed = genericDefinition.MakeGenericType(argument);
        return Activator.CreateInstance(constructed)!;
    }

    public static void TriggerAotWarning()
    {
        // IL3050: calling RequiresDynamicCode without annotation warns under AOT analyzer.
        _ = CreateGenericViaReflection(typeof(List<>), typeof(string));
    }

    [RequiresDynamicCode("Propagates AOT requirement.")]
    public static void PropagatedAotCaller()
    {
        _ = CreateGenericViaReflection(typeof(List<>), typeof(int));
    }

    // Source-generation replacement: AOT-safe alternative that avoids reflection.
    // The publish toolchain would generate the snapshot; this handwritten shape
    // represents the replacement the brief describes.
    public static string SerializeTrimSafe(TrimSample sample)
    {
        // Manual, reflection-free serialization — AOT compatible.
        return $"{{\"Name\":\"{sample.Name}\"}}";
    }

    [RequiresUnreferencedCode("Reflection-based serialization may be trimmed.")]
    [RequiresDynamicCode("Reflection-based serialization may not be AOT compatible.")]
    public static string SerializeViaReflection(object value)
    {
        var props = value.GetType().GetProperties();
        var pairs = props.Select(p => $"\"{p.Name}\":\"{p.GetValue(value)}\"");
        return "{" + string.Join(",", pairs) + "}";
    }
}
