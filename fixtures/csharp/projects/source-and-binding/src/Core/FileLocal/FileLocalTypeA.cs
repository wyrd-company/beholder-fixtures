namespace SourceBinding.Core.FileLocal;

file sealed class LocalHelper
{
    public static string Describe() => "file-local A";
}

file interface ILocalContract
{
    string Name { get; }
}

public sealed class ConsumerA : ILocalContract
{
    public string Name => LocalHelper.Describe();
}
