using System.Diagnostics.CodeAnalysis;
using System.Runtime.CompilerServices;

namespace Workshop.LowLevel;

public ref struct SpanWindow
{
    private Span<int> _window;

    public SpanWindow(Span<int> window)
    {
        _window = window;
    }

    public readonly int Length => _window.Length;

    public readonly Span<int> AsSpan() => _window;

    public ref int this[int index] => ref _window[index];

    public Span<int> Slice(int start, int length) => _window.Slice(start, length);

    public readonly ref int Front() => ref _window[0];

    [UnscopedRef]
    public ref int UnscopedFront() => ref _window[0];
}

public readonly ref struct ReadOnlyWindow
{
    private readonly Span<int> _window;

    public ReadOnlyWindow(Span<int> window)
    {
        _window = window;
    }

    public readonly int Length => _window.Length;

    public readonly ReadOnlySpan<int> AsSpan() => _window;

    public readonly ref readonly int this[int index] => ref _window[index];
}

public ref struct RefFieldContainer
{
    public ref int Ref;

    public int Tag;

    public RefFieldContainer(ref int target, int tag)
    {
        Ref = ref target;
        Tag = tag;
    }

    public void Update(int value) => Ref = value;

    public readonly int Read() => Ref;

    [UnscopedRef]
    public ref int UnscopedRef() => ref Ref;
}

public static class ScopedOperations
{
    public static void ProcessScoped(scoped ref int value)
    {
        value += 1;
    }

    public static void ProcessScopedSpan(scoped Span<int> span)
    {
        if (span.Length > 0)
        {
            span[0] += 1;
        }
    }

    public static ref int ReturnRef(ref int value) => ref value;

    public static Span<int> ReturnSpan(Span<int> span) => span;

    public static Span<int> Slice(Span<int> span, int start, int length)
        => span.Slice(start, length);

    public static void ConsumeRefField(ref RefFieldContainer container, int delta)
    {
        container.Ref += delta;
    }

    public static ref int UnwrapRefField(ref RefFieldContainer container) => ref container.Ref;

    public static Span<int> AsSpanOfWindow(ref SpanWindow window) => window.AsSpan();

    public static ReadOnlySpan<int> AsReadOnlyOfWindow(in ReadOnlyWindow window) => window.AsSpan();
}

[InlineArray(16)]
public struct InlineBuffer
{
    private int _element0;

    public void Fill(int value)
    {
        for (var i = 0; i < 16; i++)
        {
            this[i] = value;
        }
    }

    public int Sum()
    {
        var total = 0;
        foreach (var item in this)
        {
            total += item;
        }

        return total;
    }

    public void CopyFrom(ReadOnlySpan<int> source)
    {
        source.CopyTo(this);
    }
}

public static class InlineArrayUsage
{
    public static int IndexedAccess()
    {
        var buffer = new InlineBuffer();
        buffer[0] = 10;
        buffer[1] = 20;
        buffer[15] = 5;
        return buffer[0] + buffer[1] + buffer[15];
    }

    public static int SlicedSum()
    {
        var buffer = new InlineBuffer();
        buffer.Fill(2);
        Span<int> temp = buffer;
        ReadOnlySpan<int> span = temp;
        var slice = span.Slice(4, 8);
        var total = 0;
        foreach (var value in slice)
        {
            total += value;
        }

        return total;
    }

    public static void FillViaSpan(int value)
    {
        InlineBuffer buffer = default;
        Span<int> span = buffer;
        span.Fill(value);
        Span<int> destination = buffer;
        span.CopyTo(destination);
    }

    public static int SumViaSpan()
    {
        var buffer = new InlineBuffer();
        buffer.Fill(3);
        Span<int> span = buffer;
        var total = 0;
        foreach (var item in span)
        {
            total += item;
        }

        return total;
    }

    public static Span<int> BorrowSliced(ref InlineBuffer buffer, int start, int length)
    {
        Span<int> span = buffer;
        return span.Slice(start, length);
    }
}
