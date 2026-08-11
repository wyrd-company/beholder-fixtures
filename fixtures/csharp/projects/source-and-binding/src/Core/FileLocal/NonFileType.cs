namespace SourceBinding.Core.FileLocal;

public sealed class LocalHelper
{
    public static string Describe() => "non-file type";
}

public sealed class CrossFileReference
{
    // No file-local in this file, so LocalHelper resolves to the non-file type.
    public static string UseNonFile() => LocalHelper.Describe();

    public static string UseA() => ConsumerAHelper();

    private static string ConsumerAHelper() => new ConsumerA().Name;

    public static string UseB() => ConsumerB.Describe();
}
