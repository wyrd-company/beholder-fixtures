using System.Dynamic;
using Microsoft.CSharp.RuntimeBinder;

namespace GenericsAndDispatch.Core.Dynamic;

public sealed class CatalogEntry
{
    public string Title { get; set; } = string.Empty;
    public int Stock { get; set; }

    public string Describe() => $"{Title}:{Stock}";

    public string this[int index] => $"{Title}-{index}";

    public static CatalogEntry operator +(CatalogEntry left, CatalogEntry right) =>
        new() { Title = left.Title + "+" + right.Title, Stock = left.Stock + right.Stock };

    public static implicit operator string(CatalogEntry entry) => entry.Title;
}

public static class CatalogExtensions
{
    public static string Extend(this CatalogEntry entry) => $"extended:{entry.Title}";
}

public sealed class PublicDynamicHolder
{
    public dynamic Value { get; set; } = new CatalogEntry { Title = "holder", Stock = 1 };

    public dynamic Transform(dynamic input) => input;

    public static dynamic Create(dynamic input) => input;

    public dynamic Forward(dynamic input, Func<dynamic, dynamic> map) => map(input);
}

public static class DynamicExercises
{
    public static void Run()
    {
        dynamic entry = new CatalogEntry { Title = "widget", Stock = 12 };
        dynamic other = new CatalogEntry { Title = "gadget", Stock = 8 };

        // Member access, invocation, indexing.
        string title = entry.Title;
        string described = entry.Describe();
        string indexed = entry[2];

        // Operator, conversion, overload selection.
        dynamic combined = entry + other;
        string converted = (string)entry;
        dynamic overloaded = Overload((object)entry);
        dynamic dynamicOverloaded = Overload(entry);

        // Propagation: dynamic receiver propagates dynamic result.
        dynamic propagated = entry.Describe().Length;
        _ = propagated is int;

        // Dynamic nested in generics and tuples.
        List<dynamic> list = [entry, other];
        (dynamic Title, int Count) tuple = (entry, 2);
        string tupleTitle = tuple.Title.Title;

        // Public metadata and runtime binding via ExpandoObject.
        dynamic expando = new ExpandoObject();
        expando.Name = "dynamic";
        string expandoName = expando.Name;

        // Public-metadata dynamic signatures.
        dynamic holderValue = new PublicDynamicHolder().Value;
        dynamic transformed = PublicDynamicHolder.Create(entry);
        Func<dynamic, dynamic> mapper = static d => d.Title;
        dynamic forwarded = new PublicDynamicHolder().Forward(entry, mapper);
        List<dynamic> publicList = [holderValue, transformed];

        // Caught missing member via runtime binder.
        try
        {
            _ = entry.MissingMember;
        }
        catch (RuntimeBinderException)
        {
        }

        // Extension-method non-discovery: dynamic does not find extension.
        try
        {
            _ = entry.Extend();
        }
        catch (RuntimeBinderException)
        {
        }

        // Valid extension via static call still works.
        string viaStatic = CatalogExtensions.Extend(entry);

        // Explicit interface member not found via dynamic unless cast.
        dynamic identifiable = new EntryWithExplicit();
        string objectResult = DescribeObject(identifiable);
        string dynamicResult = DescribeDynamic(identifiable);
        string explicitViaCast = ((INameProvider)identifiable).Name;
        string explicitFromDynamicCast = ((INameProvider)(object)identifiable).Name;

        _ = title;
        _ = described;
        _ = indexed;
        _ = combined;
        _ = converted;
        _ = overloaded;
        _ = dynamicOverloaded;
        _ = list;
        _ = tupleTitle;
        _ = expandoName;
        _ = holderValue;
        _ = transformed;
        _ = forwarded;
        _ = publicList;
        _ = viaStatic;
        _ = objectResult;
        _ = dynamicResult;
        _ = explicitViaCast;
        _ = explicitFromDynamicCast;
    }

    private static string Overload(CatalogEntry entry) => "typed";

    private static string Overload(object value) => "object";

    private static string DescribeObject(object value) => value.ToString() ?? string.Empty;

    private static string DescribeDynamic(dynamic value) => value.Describe();
}

public sealed class EntryWithExplicit : INameProvider
{
    string INameProvider.Name => "explicit";
    public string Describe() => "explicit-entry";
}

public interface INameProvider
{
    string Name { get; }
}
