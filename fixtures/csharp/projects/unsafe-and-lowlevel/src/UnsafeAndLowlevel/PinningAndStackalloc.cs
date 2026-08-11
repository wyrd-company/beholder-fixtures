namespace Workshop.LowLevel;

public sealed class PinnableInventory
{
    private readonly int[] _items;

    public PinnableInventory(int[] items)
    {
        _items = items;
    }

    // Custom pinnable pattern: GetPinnableReference enables `fixed` over a managed type.
    public ref int GetPinnableReference() => ref _items[0];

    public int Length => _items.Length;

    public Span<int> AsSpan() => _items;
}

public static unsafe class PinningOperations
{
    public static int PinString(string text)
    {
        fixed (char* p = text)
        {
            if (p == null || text.Length == 0)
            {
                return 0;
            }

            var total = 0;
            for (var i = 0; i < text.Length; i++)
            {
                total += p[i];
            }

            return total;
        }
    }

    public static int PinEmptyString()
    {
        string text = string.Empty;
        fixed (char* p = text)
        {
            return p == null ? 0 : 1;
        }
    }

    public static int PinArray(int[] items)
    {
        if (items.Length == 0)
        {
            return 0;
        }

        fixed (int* p = items)
        {
            var total = 0;
            for (var i = 0; i < items.Length; i++)
            {
                total += p[i];
            }

            return total;
        }
    }

    public static int PinSpan(Span<int> span)
    {
        if (span.Length == 0)
        {
            return 0;
        }

        fixed (int* p = span)
        {
            var total = 0;
            for (var i = 0; i < span.Length; i++)
            {
                total += p[i];
            }

            return total;
        }
    }

    public static int PinCustomPinnable(PinnableInventory inventory)
    {
        if (inventory.Length == 0)
        {
            return 0;
        }

        fixed (int* p = inventory)
        {
            return *p;
        }
    }

    public static int PinNullArray()
    {
        int[]? items = null;
        fixed (int* p = items)
        {
            return p == null ? -1 : 0;
        }
    }

    public static int ConditionalStackalloc(int length, int fill)
    {
        // Conditional stackalloc: short buffers stay on the stack, longer ones heap-allocate.
        Span<int> buffer = length <= 64 ? stackalloc int[64] : new int[length];
        buffer = buffer.Slice(0, length);
        buffer.Fill(fill);
        var total = 0;
        foreach (var value in buffer)
        {
            total += value;
        }

        return total;
    }

    public static int UsePointerStack(int length)
    {
        Span<int> span = stackalloc int[length];
        for (var i = 0; i < span.Length; i++)
        {
            span[i] = i;
        }

        var total = 0;
        foreach (var v in span)
        {
            total += v;
        }

        return total;
    }

    public static int UseByteStack(int length)
    {
        Span<byte> span = stackalloc byte[length];
        span.Fill(0x7F);
        var total = 0;
        foreach (var b in span)
        {
            total += b;
        }

        return total;
    }

    public static int TrimStackAlloc(Span<int> input)
    {
        Span<int> workspace = stackalloc int[64];
        var usableLength = Math.Min(input.Length, workspace.Length);
        var workspaceSlice = workspace.Slice(0, usableLength);
        input.Slice(0, usableLength).CopyTo(workspaceSlice);
        var total = 0;
        foreach (var v in workspaceSlice)
        {
            total += v;
        }

        return total;
    }

    // Scoped lifetime checks: scoped parameters and ref returns that must not
    // escape the caller's stack frame are expressed through scoped/ref annotations.
    public static ref int ReturnRef(ref int value) => ref value;

    public static Span<int> ReturnSpan(Span<int> span) => span;

    public static Span<int> SliceScoped(Span<int> span, int start, int length)
        => span.Slice(start, length);

    public static ref int At(Span<int> span, int index) => ref span[index];

    public static int SumWithScopedSpan(scoped Span<int> span)
    {
        var total = 0;
        foreach (var v in span)
        {
            total += v;
        }

        return total;
    }

    public static void FillScoped(scoped Span<int> span, int value)
    {
        span.Fill(value);
    }

    public static int UseStackWithinMethod(int length)
    {
        Span<int> local = stackalloc int[length];
        for (var i = 0; i < local.Length; i++)
        {
            local[i] = i + 1;
        }

        var sum = 0;
        foreach (var v in local)
        {
            sum += v;
        }

        return sum;
    }

    public static int ConditionalBuffer(Span<int> fallback, int desiredLength)
    {
        Span<int> buffer = desiredLength <= 32 ? stackalloc int[32] : fallback.Slice(0, desiredLength);
        var usable = buffer.Slice(0, Math.Min(desiredLength, buffer.Length));
        usable.Fill(9);
        var total = 0;
        foreach (var v in usable)
        {
            total += v;
        }

        return total;
    }
}
