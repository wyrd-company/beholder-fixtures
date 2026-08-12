using SourceBinding.Extensions.CollectionOps;
using SourceBinding.Extensions.Competitive;
using SourceBinding.Extensions.RefOps;
using SourceBinding.Extensions.StringOps;

namespace SourceBinding.Core.Lookup;

public class ExtensionTarget
{
    // Instance member that wins over extension (different receiver, not competitive).
    public int WordCount() => 42;
}

public static class ExtensionLookupSurface
{
    public static int InstanceWins()
    {
        var competitive = new CompetitiveReceiver();
        int viaInstance = competitive.GetValue(); // instance wins over extension.
        int viaExtension = "hello world".WordCount(); // extension for string.
        int viaTargetInstance = new ExtensionTarget().WordCount();
        return viaInstance + viaExtension + viaTargetInstance;
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
        // Direct null receiver invocation (no conditional) – extension handles null.
        int direct = maybeNull!.WordCount();
        string? nullString = null;
        int viaDirectNull = nullString.WordCount();
        int viaStatic = SourceBinding.Extensions.StringOps.StringExtensions.WordCount(string.Empty);
        return direct + viaDirectNull + viaStatic;
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

    public static ExtensibleBag ViaExtensionAdd()
    {
        // ExtensibleBag declares no instance Add. The collection-initializer binds
        // each element through the extension Add, and the direct call form resolves
        // to the same extension. Extension-mediated Add participates in lookup.
        var bag = new ExtensibleBag { 1, 2 };
        bag.Add(3);

        // Extension AddRange participates on ICollection<T>, which has no instance
        // AddRange, while List<T>'s instance Add is used inside the extension.
        System.Collections.Generic.ICollection<int> collection = new List<int> { 1, 2 };
        collection.AddRange(new[] { 3, 4 });

        return bag;
    }
}


