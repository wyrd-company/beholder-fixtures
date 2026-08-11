using System.Diagnostics.CodeAnalysis;

namespace Acme.Deployment.Trimming;

public class TrimSample
{
    public string Name { get; set; } = "default";
    public string Describe() => $"TrimSample:{Name}";
    private string HiddenNote => "hidden";
    public static string StaticHelper() => "static";
}

public class TrimHiddenTarget
{
    public string Secret { get; set; } = "secret";
}

public static class TrimmingAnnotations
{
    // RequiresUnreferencedCode — trimming may remove members accessed via string.
    [RequiresUnreferencedCode("Type resolution by name may be trimmed.")]
    public static object? CreateByTypeName(string assemblyQualifiedName)
    {
        var type = Type.GetType(assemblyQualifiedName);
        return type is null ? null : Activator.CreateInstance(type);
    }

    // DynamicallyAccessedMembers — preserves members on the annotated type parameter.
    public static void CreateWithDynamicallyAccessed(
        [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors)] Type type)
    {
        _ = Activator.CreateInstance(type);
    }

    public static void CreateWithPublicMethods(
        [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicMethods)] Type type)
    {
        var method = type.GetMethod("Describe");
        _ = method;
    }

    // DynamicDependency — explicitly roots a member for the trimmer.
    [DynamicDependency(DynamicallyAccessedMemberTypes.PublicMethods, typeof(TrimSample))]
    public static void UseWithDynamicDependency()
    {
        // TrimSample.Describe is kept via the attribute; no direct call needed.
    }

    // Intentionally unannotated — the trimming analyzer will warn at the call site
    // when RequiresUnreferencedCode is consumed without propagation.
    public static void TriggerTrimWarning()
    {
        // IL2026: calling RequiresUnreferencedCode member without annotation.
        _ = CreateByTypeName("Acme.Deployment.Trimming.TrimSample, Trimming");
    }

    // Correctly annotated consumer — no warning when the caller propagates the attribute.
    [RequiresUnreferencedCode("Propagates trim requirement.")]
    public static void PropagatedCaller()
    {
        _ = CreateByTypeName("Acme.Deployment.Trimming.TrimSample, Trimming");
    }

    // Missing member after trim — valid source that would fail only at trimmed runtime.
    [RequiresUnreferencedCode("Accesses member that trimming may remove.")]
    public static string AccessPotentiallyTrimmedMember(
        [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicProperties)] Type t)
    {
        var prop = t.GetProperty("Name");
        return prop?.GetValue(Activator.CreateInstance(t))?.ToString() ?? "missing";
    }

    // Genuinely missing after trim: no DynamicallyAccessedMembers preservation, so
    // the trimmer may remove TrimHiddenTarget.Secret and the lookup returns null at trimmed runtime.
    // Preserved path above keeps TrimSample.Name; this unpreserved path may lose Secret.
    [RequiresUnreferencedCode("Member lookup by raw string may be trimmed; 'Secret' may be absent after trim.")]
    public static string AccessViaRawStringMayBeMissing(Type t)
    {
        var prop = t.GetProperty("Secret");
        return prop?.GetValue(Activator.CreateInstance(t))?.ToString() ?? "missing";
    }
}
