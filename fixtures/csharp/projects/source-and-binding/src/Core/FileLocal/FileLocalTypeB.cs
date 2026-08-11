namespace SourceBinding.Core.FileLocal;

file sealed class LocalHelper
{
    public static string Describe() => "file-local B";
}

public sealed class ConsumerB
{
    public static string Describe() => LocalHelper.Describe();
}
