namespace SourceBinding.NoImplicit;

public sealed class Consumer
{
    public static string Describe() => ExplicitGlobalUsings.BuildList().FirstOrDefault() ?? "none";
}
