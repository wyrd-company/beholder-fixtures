namespace Acme.Identity;

public sealed class SharedWidget
{
    public string Origin => "Identity.SignedLibrary v2.0.0 signed";
    public static string AssemblyName => typeof(SharedWidget).Assembly.GetName().Name!;
    public bool IsSigned => (typeof(SharedWidget).Assembly.GetName().GetPublicKey()?.Length ?? 0) > 0;
}
