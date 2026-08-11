namespace Fixture.AttributesAndMetadata.Contexts.Documentation;

/// <summary>
/// Demonstrates symbols named outside executable expressions:
/// <see langword="nameof"/>, <see langword="typeof"/> (including open and
/// closed generic type objects), and documentation <c>cref</c> references
/// such as this one to <see cref="Describe(int)"/>, <see cref="Sample"/>,
/// and <see cref="Container{T}"/>. Built with <c>GenerateDocumentationFile</c>
/// enabled so this comment is emitted as XML documentation output.
/// </summary>
public static class SymbolNamingDemo
{
    /// <summary>
    /// Returns the simple name of <paramref name="value"/>'s declaring
    /// parameter captured via <see langword="nameof"/>, alongside the
    /// runtime <see cref="Type"/> captured via <see langword="typeof"/>.
    /// </summary>
    /// <param name="value">The described value.</param>
    public static string Describe(int value)
        => $"{nameof(value)}={value} type={typeof(int).Name}";

    /// <summary>Represents a labeled sample value.</summary>
    public sealed class Sample
    {
        /// <summary>Gets the label.</summary>
        public string Label { get; init; } = string.Empty;
    }

    /// <summary>A generic container referenced by both its open and closed generic type objects.</summary>
    /// <typeparam name="T">The contained value's type.</typeparam>
    public sealed class Container<T>
    {
        /// <summary>Gets or sets the contained value.</summary>
        public T? Value { get; set; }
    }

    /// <summary>
    /// Captures the open generic type object via <c>typeof(Container&lt;&gt;)</c>
    /// and the closed generic type object via <c>typeof(Container&lt;int&gt;)</c>.
    /// </summary>
    public static string DescribeGenericTypeObjects()
    {
        var openGeneric = typeof(Container<>);
        var closedGeneric = typeof(Container<int>);
        return $"open-is-definition={openGeneric.IsGenericTypeDefinition} closed-is-definition={closedGeneric.IsGenericTypeDefinition}";
    }
}
