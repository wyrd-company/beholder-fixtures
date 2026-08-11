using Fixture.AttributesAndMetadata.Core.Attributes;

namespace Fixture.AttributesAndMetadata.Core.Reflection;

/// <summary>A file-local type (C# 11+), marked so it can be located without depending on its emitted name shape.</summary>
[Showcase("file-local-target")]
file sealed class FileLocalObservable
{
}

/// <summary>
/// Locates the file-local type declared above purely by its
/// <see cref="ShowcaseAttribute"/> marker and label, never by matching its
/// synthesized metadata name, per CS-CAN-125.
/// </summary>
public static class FileLocalTypeObservation
{
    public static string DescribeFileLocalType()
    {
        var type = typeof(FileLocalTypeObservation).Assembly
            .GetTypes()
            .FirstOrDefault(t => t.GetCustomAttributes(typeof(ShowcaseAttribute), false)
                .Cast<ShowcaseAttribute>()
                .Any(a => a.Label == "file-local-target"));

        return type is null
            ? "no-file-local-type-found"
            : $"file-local-type-present is-public={type.IsPublic}";
    }
}
