using System.Text.RegularExpressions;

namespace Catalog.Web.Text;

public partial class CatalogPatterns
{
    [GeneratedRegex(@"^[A-Z]{2,4}-\d{4}$", RegexOptions.IgnoreCase)]
    public static partial Regex CatalogCode();

    [GeneratedRegex(@"^CAT-\d{3}$", RegexOptions.None)]
    public static partial Regex ShortCode();

    public static readonly Regex RuntimeCatalogCode = new(@"^[A-Z]{2,4}-\d{4}$", RegexOptions.IgnoreCase | RegexOptions.Compiled);

    public static readonly Regex RuntimeShortCode = new(@"^CAT-\d{3}$", RegexOptions.None);

    public static bool IsValidCatalogCode(string input) => CatalogCode().IsMatch(input);

    public static bool IsValidShortCode(string input) => ShortCode().IsMatch(input);

    public static bool IsValidCatalogCodeRuntime(string input) => RuntimeCatalogCode.IsMatch(input);

    public static bool IsValidShortCodeRuntime(string input) => RuntimeShortCode.IsMatch(input);

    public static string NormalizeCode(string input)
    {
        var match = CatalogCode().Match(input);
        return match.Success ? match.Value.ToUpperInvariant() : input;
    }
}
