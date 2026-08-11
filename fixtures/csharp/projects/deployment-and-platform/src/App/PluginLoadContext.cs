using System.Reflection;
using System.Runtime.Loader;

namespace Acme.Deployment.App;

public class PluginLoadContext : AssemblyLoadContext
{
    private readonly AssemblyDependencyResolver _resolver;

    public PluginLoadContext(string pluginPath) : base(isCollectible: true)
    {
        _resolver = new AssemblyDependencyResolver(pluginPath);
    }

    protected override Assembly? Load(AssemblyName assemblyName)
    {
        var path = _resolver.ResolveAssemblyToPath(assemblyName);
        if (path is not null)
        {
            return LoadFromAssemblyPath(path);
        }

        return null;
    }

    public static Assembly LoadPluginAssembly(string pluginPath)
    {
        var context = new PluginLoadContext(pluginPath);
        return context.LoadFromAssemblyPath(pluginPath);
    }

    public static string DescribeLoadContext(Assembly assembly)
    {
        var alc = AssemblyLoadContext.GetLoadContext(assembly);
        return alc?.Name ?? alc?.ToString() ?? "default-context";
    }

    // Runtime assembly graph differs from compile graph:
    // App references Contracts at compile time but not Plugin; Plugin is present only at runtime.
    public static bool IsPluginReferencedAtCompileTime()
    {
        var referenced = typeof(Program).Assembly.GetReferencedAssemblies();
        return referenced.Any(a => a.Name == "Plugin");
    }

    public static string[] ReferencedAssemblyNames() =>
        typeof(Program).Assembly.GetReferencedAssemblies().Select(a => a.Name ?? "").ToArray();
}
