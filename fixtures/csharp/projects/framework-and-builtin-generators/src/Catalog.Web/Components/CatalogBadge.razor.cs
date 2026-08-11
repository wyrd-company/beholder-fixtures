using Microsoft.AspNetCore.Components;

namespace Catalog.Web.Components;

public partial class CatalogBadge : ComponentBase
{
    [Parameter]
    public string Title { get; set; } = string.Empty;

    [Parameter]
    public string Subtitle { get; set; } = string.Empty;

    public string FormatBadge() => $"{Title} — {Subtitle}";
}
