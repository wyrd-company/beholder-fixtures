namespace Catalog.FunctionsAndAsync.Foreach;

public sealed class PatternOnlyCollection
{
    private readonly int[] _values;

    public PatternOnlyCollection(params int[] values) => _values = values;

    public PatternEnumerator GetEnumerator() => new(_values);
}

public struct PatternEnumerator
{
    private readonly int[] _values;
    private int _index;

    public PatternEnumerator(int[] values)
    {
        _values = values;
        _index = -1;
    }

    public int Current => _values[_index];

    public bool MoveNext()
    {
        _index++;
        return _index < _values.Length;
    }
}

public sealed class DisposablePatternCollection : IDisposable
{
    private readonly int[] _values;

    public DisposablePatternCollection(params int[] values) => _values = values;

    public DisposablePatternEnumerator GetEnumerator() => new(_values);

    public void Dispose() { }
}

public struct DisposablePatternEnumerator : IDisposable
{
    private readonly int[] _values;
    private int _index;

    public DisposablePatternEnumerator(int[] values)
    {
        _values = values;
        _index = -1;
    }

    public int Current => _values[_index];

    public bool MoveNext()
    {
        _index++;
        return _index < _values.Length;
    }

    public void Dispose() { }
}

public struct StructEnumeratorCollection
{
    private readonly int[] _values;

    public StructEnumeratorCollection(params int[] values) => _values = values;

    public StructEnumerator GetEnumerator() => new(_values);

    public struct StructEnumerator
    {
        private readonly int[] _values;
        private int _index;

        public StructEnumerator(int[] values)
        {
            _values = values;
            _index = -1;
        }

        public int Current => _values[_index];

        public bool MoveNext()
        {
            _index++;
            return _index < _values.Length;
        }
    }
}

public sealed class RefStructPatternCollection
{
    private readonly int[] _values;

    public RefStructPatternCollection(params int[] values) => _values = values;

    public RefStructEnumerator GetEnumerator() => new(_values);
}

public ref struct RefStructEnumerator
{
    private readonly int[] _values;
    private int _index;

    public RefStructEnumerator(int[] values)
    {
        _values = values;
        _index = -1;
    }

    public int Current => _values[_index];

    public bool MoveNext()
    {
        _index++;
        return _index < _values.Length;
    }

    public void Dispose() { }
}

public sealed class BoxingStructCollection
{
    private readonly int[] _values;

    public BoxingStructCollection(params int[] values) => _values = values;

    public BoxingStructEnumerator GetEnumerator() => new(_values);

    public struct BoxingStructEnumerator : IDisposable
    {
        private readonly int[] _values;
        private int _index;

        public BoxingStructEnumerator(int[] values)
        {
            _values = values;
            _index = -1;
        }

        public int Current => _values[_index];

        public bool MoveNext()
        {
            _index++;
            return _index < _values.Length;
        }

        public void Dispose() { }
    }
}

public sealed class PlainCollection
{
    private readonly int[] _values;

    public PlainCollection(params int[] values) => _values = values;
}

public static class ExtensionEnumeration
{
    public static ExtensionEnumerator GetEnumerator(this PlainCollection source) =>
        new(source);

    public sealed class ExtensionEnumerator
    {
        private readonly int[] _values;
        private int _index;

        public ExtensionEnumerator(PlainCollection source)
        {
            var field = typeof(PlainCollection).GetField("_values", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)!;
            _values = (int[])field.GetValue(source)!;
            _index = -1;
        }

        public int Current => _values[_index];

        public bool MoveNext()
        {
            _index++;
            return _index < _values.Length;
        }
    }
}
