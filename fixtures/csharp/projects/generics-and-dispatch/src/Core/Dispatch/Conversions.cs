namespace GenericsAndDispatch.Core.Dispatch;

public enum OrderStatus { Pending = 0, Active = 1, Closed = 2 }

public sealed class CatalogItem : IComparable<CatalogItem>
{
    public string Name { get; init; }
    public CatalogItem(string name) => Name = name;
    public int CompareTo(CatalogItem? other) => string.Compare(Name, other?.Name, StringComparison.Ordinal);
}

public readonly struct Currency : IEquatable<Currency>
{
    public decimal Amount { get; }
    public Currency(decimal amount) => Amount = amount;
    public bool Equals(Currency other) => Amount == other.Amount;
    public override bool Equals(object? obj) => obj is Currency other && Equals(other);
    public override int GetHashCode() => Amount.GetHashCode();

    public static implicit operator decimal(Currency currency) => currency.Amount;
    public static explicit operator Currency(decimal amount) => new(amount);
    public static explicit operator Currency(int amount) => new(amount);
}

public static class ConversionExercises
{
    public static void Run()
    {
        // Identity and numeric/constant conversions.
        int i = 42;
        long l = i;
        long big = int.MaxValue + 10L;
        try
        {
            int narrowedOverflow = checked((int)big);
            _ = narrowedOverflow;
        }
        catch (OverflowException)
        {
        }

        const int constant = 100;
        byte asByte = constant;
        double d = 3.14;

        // Enum conversions.
        OrderStatus status = OrderStatus.Active;
        int asInt = (int)status;
        OrderStatus fromInt = (OrderStatus)asInt;

        // Reference and variance conversions.
        object boxedObject = new CatalogItem("alpha");
        CatalogItem downcast = (CatalogItem)boxedObject;
        try
        {
            object notCatalog = "string";
            CatalogItem failedDowncast = (CatalogItem)notCatalog;
            _ = failedDowncast;
        }
        catch (InvalidCastException)
        {
        }

        IEnumerable<CatalogItem> items = [new CatalogItem("a")];
        IEnumerable<object> objects = items;

        // Boxing/unboxing, including invalid numeric unbox.
        object boxed = 5;
        int unboxed = (int)boxed;
        try
        {
            object boxedDouble = 5.0;
            int invalidUnbox = (int)boxedDouble;
            _ = invalidUnbox;
        }
        catch (InvalidCastException)
        {
        }

        object boxedEnum = OrderStatus.Active;
        OrderStatus unboxedEnum = (OrderStatus)boxedEnum;

        // User-defined conversion interaction.
        Currency currency = (Currency)10.5m;
        decimal asDecimal = currency;
        Currency fromDecimal = (Currency)5;
        string userConversionOverload = Overload(currency);
        string userConversionViaDecimal = Overload((decimal)currency);

        // Nullable conversions and tuple conversions.
        int? nullableInt = 5;
        int? lifted = nullableInt + 2;
        (int Number, string Label) tuple = (7, "ok");
        (long Number, string Label) widenedTuple = tuple;

        // Dynamic conversion.
        dynamic dyn = "dynamic";
        string fromDynamic = (string)dyn;

        // Pointer conversion (requires unsafe; identity via void*).
        unsafe
        {
            int value = 7;
            int* pointer = &value;
            void* voidPointer = pointer;
            int* roundTripped = (int*)voidPointer;
            _ = roundTripped;
        }

        // Method-group/lambda conversions via delegate target.
        Func<int, int> methodGroup = Identity;
        Func<int, int> lambda = x => x + 1;

        // Span conversion.
        int[] array = [1, 2, 3];
        Span<int> span = array;
        ReadOnlySpan<int> roSpan = array;

        // Interpolation-handler conversion.
        string interpolated = $"value:{i}";
        FormattableString formattable = $"value:{i}";

        // Null literal conversion.
        string? maybeNull = null;
        object? maybeObject = maybeNull;

        // Is/as with built-in only (not user conversion).
        bool isString = maybeObject is string;
        string? asString = maybeObject as string;

        _ = l; _ = asByte; _ = d;
        _ = downcast; _ = objects; _ = unboxed; _ = unboxedEnum;
        _ = currency; _ = asDecimal; _ = fromDecimal; _ = userConversionOverload; _ = userConversionViaDecimal;
        _ = lifted; _ = widenedTuple; _ = fromDynamic;
        _ = methodGroup; _ = lambda; _ = span; _ = roSpan;
        _ = interpolated; _ = formattable; _ = isString; _ = asString;
    }

    private static int Identity(int value) => value;

    private static string Overload(Currency currency) => $"currency:{currency.Amount}";
    private static string Overload(decimal value) => $"decimal:{value}";

    public static bool TryUnbox(object boxed, out int value)
    {
        if (boxed is int i)
        {
            value = i;
            return true;
        }

        value = 0;
        return false;
    }
}
