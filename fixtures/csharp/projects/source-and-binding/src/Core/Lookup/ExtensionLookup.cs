using SourceBinding.Extensions.StringOps;
using SourceBinding.Extensions.CollectionOps;
using SourceBinding.Extensions.RefOps;
// Note: CompetingA vs CompetingB drives import-based binding; only one is imported per file.

namespace SourceBinding.Core.Lookup;

public class ExtensionTarget
{
    // Instance member that wins over extension.
    public int WordCount() => 42;
}

public static class ExtensionLookupSurface
{
    public static int InstanceWins()
    {
        var target = new ExtensionTarget();
        int viaExtension = "hello world".WordCount(); // extension.
        int viaInstance = target.WordCount(); // instance wins.
        return viaExtension + viaInstance;
    }

    public static int ViaGenericAndInterface()
    {
        List<string> list = new List<string> { "a", "b", "c" };
        string? first = list.FirstOrDefaultCustom();
        int count = list.CountWhere(s => s.Length == 1);
        _ = first;
        return count;
    }

    public static void ViaRef()
    {
        int value = 5;
        value.Increment(); // ref receiver.
        int copy;
        value.ReadOnlyView(out copy);
        _ = copy;
    }

    public static int ViaNullReceiver()
    {
        string? maybeNull = null;
        // Null receiver is allowed; extension handles null.
        int length = maybeNull?.WordCount() ?? -1;
        int viaStatic = SourceBinding.Extensions.StringOps.StringExtensions.WordCount(maybeNull ?? string.Empty);
        return length + viaStatic;
    }

    public static int ViaStaticCall()
    {
        // Static-call form versus instance-call form.
        string text = "hello world";
        int viaInstance = text.WordCount();
        int viaStatic = SourceBinding.Extensions.StringOps.StringExtensions.WordCount(text);
        return viaInstance + viaStatic;
    }

    public static void ViaMethodGroup()
    {
        Func<string, int> group = SourceBinding.Extensions.StringOps.StringExtensions.WordCount;
        Func<string, int> viaDelegate = group;
        _ = viaDelegate("a b c");
    }

    public static void ViaExtensionAdd()
    {
        List<int> list = new List<int> { 1, 2 };
        list.AddRange(new[] { 3, 4 }); // extension AddRange via CollectionOps.
    }
}


