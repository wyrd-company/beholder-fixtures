namespace Acme.Identity;

public sealed class SharedWidget
{
    public string Origin => "Identity.LibraryB v1.0.0";
    public static string AssemblyName => typeof(SharedWidget).Assembly.GetName().Name!;
    public string Describe() => $"Widget from {AssemblyName} v{typeof(SharedWidget).Assembly.GetName().Version}";
}
