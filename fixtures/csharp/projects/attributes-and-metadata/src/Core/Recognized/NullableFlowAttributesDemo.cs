using System.Diagnostics.CodeAnalysis;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// Exercises the compiler-recognized nullable-flow attributes: a
/// <c>TryGetValue</c>-shaped method with <see cref="NotNullWhenAttribute"/>,
/// an initializer with <see cref="MemberNotNullAttribute"/>, a
/// non-returning helper with <see cref="DoesNotReturnAttribute"/>, a
/// property with <see cref="AllowNullAttribute"/>, and a method with a
/// <see cref="MaybeNullAttribute"/>-annotated return value.
/// </summary>
public sealed class NullableFlowShowcase
{
    private string? _value;
    private string? _display;

    [MemberNotNull(nameof(_value))]
    public void Initialize(string value) => _value = value;

    public static bool TryGetValue(string? input, [NotNullWhen(true)] out string? result)
    {
        result = input;
        return input is not null;
    }

    [DoesNotReturn]
    public static void Fail(string message) => throw new InvalidOperationException(message);

    [AllowNull]
    public string Display
    {
        get => _display ?? string.Empty;
        set => _display = value;
    }

    [return: MaybeNull]
    public static string FindOrDefault(bool found) => found ? "found" : default!;
}
