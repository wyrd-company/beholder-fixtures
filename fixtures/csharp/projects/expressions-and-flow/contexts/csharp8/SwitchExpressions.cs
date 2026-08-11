using System;

namespace ExpressionsFlow.CSharp8
{
    public enum StatusKind
    {
        Pending,
        Active,
        Retired,
    }

    public sealed class Item
    {
        public Item(string label, int count)
        {
            Label = label;
            Count = count;
        }

        public string Label { get; }

        public int Count { get; }
    }

    public static class SwitchExpressions
    {
        public static string Describe(StatusKind kind)
        {
            return kind switch
            {
                StatusKind.Pending => "pending",
                StatusKind.Active => "active",
                StatusKind.Retired => "retired",
                _ => "unknown",
            };
        }

        public static string Classify(int? value)
        {
            return value switch
            {
                null => "none",
                0 => "zero",
                int n when n > 0 => "positive",
                _ => "negative",
            };
        }

        public static bool IsStock(Item item)
        {
            return item switch
            {
                { Label: "stock" } => true,
                _ => false,
            };
        }
    }
}
