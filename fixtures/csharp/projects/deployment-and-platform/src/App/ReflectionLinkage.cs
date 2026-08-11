using System.Diagnostics.CodeAnalysis;
using System.Reflection;
using Acme.Deployment.Contracts;

namespace Acme.Deployment.App;

public static class ReflectionLinkage
{
    // Raw string resolution — trimmable, compared with nameof below.
    [RequiresUnreferencedCode("Resolves type by raw string.")]
    public static Type? ResolveByRawString()
    {
        return Type.GetType("Acme.Deployment.Trimming.TrimSample, Trimming");
    }

    // nameof-based type name — compiler-bound reference, survives renaming.
    public static Type? ResolveByNameof()
    {
        var name = typeof(Acme.Deployment.Trimming.TrimSample).FullName;
        return Type.GetType($"{name}, Trimming");
    }

    private static string TypeNameViaNameof() => typeof(Acme.Deployment.Trimming.TrimSample).FullName!;

    public static string DescribeNameofVersusRaw()
    {
        var viaNameof = TypeNameViaNameof();
        const string raw = "Acme.Deployment.Trimming.TrimSample";
        // nameof yields the final identifier; raw string is not compiler-checked.
        var viaNameofIdentifier = nameof(Acme.Deployment.Trimming.TrimSample);
        return $"{viaNameof}|{raw}|{viaNameofIdentifier}";
    }

    // Dynamic instantiation via Activator — trimmable path.
    [RequiresUnreferencedCode("Creates instance via reflection.")]
    public static object? CreateViaActivator(string typeName)
    {
        var t = Type.GetType(typeName);
        return t is null ? null : Activator.CreateInstance(t);
    }

    [RequiresUnreferencedCode("Creates instance via reflection.")]
    public static object? CreateViaActivatorGeneric(
        [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicParameterlessConstructor)] Type type)
    {
        return Activator.CreateInstance(type);
    }

    // Private member reflection — NonPublic access.
    [RequiresUnreferencedCode("Accesses private member.")]
    public static object? InvokePrivateMember(object target, string methodName)
    {
        var method = target.GetType().GetMethod(methodName, BindingFlags.Instance | BindingFlags.NonPublic);
        return method?.Invoke(target, null);
    }

    // Member access by nameof vs raw string.
    public static string AccessMemberByNameof(Trimming.TrimSample sample)
    {
        var propName = nameof(Trimming.TrimSample.Name);
        var prop = typeof(Trimming.TrimSample).GetProperty(propName);
        return prop?.GetValue(sample)?.ToString() ?? "missing";
    }

    [RequiresUnreferencedCode("Member access by raw string may be trimmed.")]
    public static string AccessMemberByRawString(object target, string memberName)
    {
        var method = target.GetType().GetMethod(memberName);
        return method?.Invoke(target, null)?.ToString() ?? "missing";
    }

    // Missing / ambiguous names — valid source that handles the failure at runtime.
    public static bool TryResolveMissing(out Type? type)
    {
        type = Type.GetType("Acme.Deployment.MissingType, Trimming");
        return type is not null;
    }

    public static bool TryResolveAmbiguous()
    {
        // Two types with the same name in different assemblies would be ambiguous;
        // here we demonstrate the null/missing path the runtime would take.
        var t = Type.GetType("Acme.Deployment.AmbiguousType, DoesNotExist");
        return t is null;
    }

    // Plugin discovery by string — plugin loaded via ALC, discovered by interface name.
    [RequiresUnreferencedCode("Discovers plugin types by reflection.")]
    public static IEnumerable<IPlugin> DiscoverPlugins(Assembly assembly)
    {
        foreach (var type in assembly.GetTypes())
        {
            if (typeof(IPlugin).IsAssignableFrom(type) && !type.IsAbstract)
            {
                if (Activator.CreateInstance(type) is IPlugin plugin)
                {
                    yield return plugin;
                }
            }
        }
    }

    // Trimming-aware variant with DynamicallyAccessedMembers on the assembly's types.
    [RequiresUnreferencedCode("Discovers plugin types by reflection.")]
    public static IEnumerable<IPlugin> DiscoverPluginsTrimAware(
        [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicConstructors | DynamicallyAccessedMemberTypes.PublicMethods)]
        Type pluginBase)
    {
        // The attribute preserves constructors; body still reflects.
        _ = pluginBase;
        return [];
    }
}
