using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Catalog.Web.Pages;

public sealed class EntryModel : PageModel
{
    public string EntryName { get; set; } = "Sample Entry";

    public decimal Price { get; set; } = 9.99m;

    public IReadOnlyList<string> Tags { get; } = new[] { "sample", "catalog", "web" };

    public void OnGet()
    {
    }

    public string FormatHeading() => $"Entry: {EntryName} ({Price:C})";
}
