using System.Diagnostics.CodeAnalysis;
using System.Text.Json;

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

    // Source-generation replacement: AOT-safe path via System.Text.Json source generator.
    // The JsonSerializerContext is generated in-process during publish/build.
    public static string SerializeTrimSafe(TrimSample sample)
    {
        return JsonSerializer.Serialize(sample, WorkshopJsonContext.Default.TrimSample);
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
