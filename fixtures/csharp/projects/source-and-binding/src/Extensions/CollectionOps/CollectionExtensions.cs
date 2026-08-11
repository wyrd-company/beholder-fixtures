using System;
using System.Collections.Generic;

namespace SourceBinding.Extensions.CollectionOps;

public static class CollectionExtensions
{
    public static void AddRange<T>(this ICollection<T> source, IEnumerable<T> items)
    {
        foreach (var item in items)
        {
            source.Add(item);
        }
    }

    public static T FirstOrDefaultCustom<T>(this IEnumerable<T> source) where T : class
    {
        foreach (var item in source)
        {
            return item;
        }

        return default!;
    }

    public static int CountWhere<T>(this IEnumerable<T> source, Func<T, bool> predicate)
    {
        int count = 0;
        foreach (var item in source)
        {
            if (predicate(item))
            {
                count++;
            }
        }

        return count;
    }
}
