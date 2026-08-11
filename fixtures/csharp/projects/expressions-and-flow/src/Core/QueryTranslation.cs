namespace ExpressionsFlow.Core;

public sealed record LedgerEntry(string Category, int Amount, int Quantity);

public sealed class LedgerStore
{
    private readonly List<LedgerEntry> _entries;

    public LedgerStore(IEnumerable<LedgerEntry> entries) => _entries = entries.ToList();

    public IEnumerable<LedgerEntry> Entries => _entries;
}

// Custom query-pattern type (instance binding vs extension binding)
public sealed class CatalogQuery<T> : IEnumerable<T>
{
    private readonly IEnumerable<T> _source;

    public CatalogQuery(IEnumerable<T> source) => _source = source;

    public IEnumerator<T> GetEnumerator() => _source.GetEnumerator();

    System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();

    // Instance Where/Select are preferred over extension when present
    public CatalogQuery<T> Where(Func<T, bool> predicate) => new(_source.Where(predicate));

    public CatalogQuery<TResult> Select<TResult>(Func<T, TResult> selector) =>
        new(_source.Select(selector));

    public CatalogQuery<U> SelectMany<U>(Func<T, IEnumerable<U>> selector) =>
        new(_source.SelectMany(selector));

    // Used for query translation of let / join / group
    public CatalogQuery<TResult> SelectMany<U, TResult>(Func<T, IEnumerable<U>> collectionSelector, Func<T, U, TResult> resultSelector) =>
        new(_source.SelectMany(collectionSelector, resultSelector));

    public CatalogQuery<T> OrderBy<TKey>(Func<T, TKey> keySelector) =>
        new(_source.OrderBy(keySelector));

    public CatalogQuery<T> OrderByDescending<TKey>(Func<T, TKey> keySelector) =>
        new(_source.OrderByDescending(keySelector));

    public IGrouping<TKey, T> GroupBy<TKey>(Func<T, TKey> keySelector) =>
        throw new NotSupportedException();

    // To materialize
    public List<T> ToList() => _source.ToList();
}

public static class QueryTranslation
{
    // Basic from / where / select over enumerable
    public static IEnumerable<string> FilterAndSelect(IEnumerable<LedgerEntry> entries)
    {
        var q = from e in entries
                where e.Amount > 10
                select e.Category;
        return q;
    }

    // Multiple from (SelectMany) and let (transparent identifier)
    public static IEnumerable<string> MultipleFromAndLet(IEnumerable<LedgerEntry> entries)
    {
        var q = from e in entries
                from c in e.Category
                let doubled = e.Amount * 2
                where doubled > 20
                select $"{c}:{doubled}";
        return q;
    }

    // Join / group / into / orderby
    public static IEnumerable<IGrouping<string, LedgerEntry>> GroupAndJoin(IEnumerable<LedgerEntry> entries, IEnumerable<LedgerEntry> other)
    {
        var grouped = from e in entries
                      group e by e.Category into g
                      orderby g.Key
                      select g;
        // Join form
        var joined = from e in entries
                     join o in other on e.Category equals o.Category
                     select e;
        _ = joined.Count();
        return grouped;
    }

    // Query over queryable (expression trees)
    public static IQueryable<string> QueryableTranslation(IQueryable<LedgerEntry> entries)
    {
        var q = from e in entries
                where e.Amount > 5
                orderby e.Category
                select e.Category;
        return q;
    }

    // Custom query-pattern type
    public static CatalogQuery<string> CustomQuery(CatalogQuery<LedgerEntry> query)
    {
        var q = from e in query
                where e.Amount > 10
                let label = e.Category.ToUpperInvariant()
                orderby label
                select label;
        return q;
    }

    // Transparent identifiers lowered to SelectMany with anonymous type
    public static IEnumerable<string> TransparentIdentifiers(IEnumerable<LedgerEntry> entries)
    {
        var q = from e in entries
                let upper = e.Category.ToUpperInvariant()
                where upper.Length > 2
                select upper;
        return q;
    }

    // Typed-range Cast: from x in (IEnumerable) ... would require Cast<T>
    public static IEnumerable<int> CastRange(System.Collections.IEnumerable untyped)
    {
        var q = from int item in untyped.Cast<int>()
                where item > 5
                select item;
        return q;
    }

    // Instance versus extension binding: CatalogQuery<T> has instance Where/Select,
    // so query on CatalogQuery resolves to instance members, not Enumerable extensions.
    public static CatalogQuery<string> InstanceBinding(CatalogQuery<LedgerEntry> source)
    {
        return from e in source
               where e.Amount > 2
               select e.Category;
    }

    // Delegate versus expression-tree selection: enumerable Where expects delegate,
    // queryable Where expects expression tree.
    public static int DelegateVsExpressionCount(IEnumerable<LedgerEntry> enumerable, IQueryable<LedgerEntry> queryable)
    {
        int del = enumerable.Where(e => e.Amount > 3).Count();
        int expr = queryable.Where(e => e.Amount > 3).Count();
        return del + expr;
    }

    // Missing-import failure and dynamic rejection are diagnostics:
    //   var q = from e in entries where e.Amount > 5 select e; // requires System.Linq import for Where/Select
    //   dynamic dyn = entries;
    //   var q2 = from e in dyn select e; // CS1979 query over dynamic is not supported
}

public static class QueryExercises
{
    public static int Run()
    {
        var entries = new[]
        {
            new LedgerEntry("alpha", 10, 2),
            new LedgerEntry("beta", 30, 5),
            new LedgerEntry("alpha", 50, 1),
        };

        int a = QueryTranslation.FilterAndSelect(entries).Count();
        int b = QueryTranslation.MultipleFromAndLet(entries).Count();
        int c = QueryTranslation.GroupAndJoin(entries, entries).Count();
        int d = QueryTranslation.CustomQuery(new CatalogQuery<LedgerEntry>(entries)).ToList().Count;
        int e = QueryTranslation.TransparentIdentifiers(entries).Count();
        int f = QueryTranslation.CastRange(entries.Select(x => (object)x.Amount).ToArray()).Count();
        return a + b + c + d + e + f;
    }
}
