namespace Acme.ReferenceAssemblyDemo;

public sealed class ReferenceFeature
{
    public string Message => "Implementation assembly feature";
    public int Compute(int input) => input * 2;
    internal string InternalDetail => "internal detail not in ref assembly";
    private string PrivateDetail => "private not in ref assembly";
}

public static class FrameworkPackProbe
{
    // Compiled against net10.0 reference pack (Microsoft.NETCore.App.Ref) and runs
    // on the implementation pack (Microsoft.NETCore.App). This type uses only BCL
    // APIs available in the reference pack.
    public static string DescribePack() => "net10.0 reference vs implementation packs";
}
