namespace SourceBinding.CSharp11;

file sealed class LocalHelper
{
    public static string Describe() => "file-local helper C#11 B";
}

public sealed class ConsumerB11
{
    public static string Describe() => LocalHelper.Describe();
}
