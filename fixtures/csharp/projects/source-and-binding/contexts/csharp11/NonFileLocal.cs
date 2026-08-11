namespace SourceBinding.CSharp11;

public sealed class LocalHelper
{
    public static string Describe() => "non-file helper C#11";
}

public sealed class CrossReference11
{
    public static string UseNonFile() => LocalHelper.Describe();
}
