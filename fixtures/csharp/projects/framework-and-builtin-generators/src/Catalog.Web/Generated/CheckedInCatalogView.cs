// Checked-in generated file for CS-CAN-122 contrast.
// This file represents the committed output of a previous markup generation run
// for a catalog view. The live Razor page at Pages/Entry.cshtml generates its
// C# to the build intermediate output (obj/) and is not committed. Together
// they demonstrate the checked-in-versus-build-generated contrast required by
// CS-CAN-122. Neither file is rewritten by the required build/lint/test tasks.

namespace Catalog.Web.Generated;

/// <summary>
/// Checked-in generated catalog view. The generator that produced this file
/// emitted a partial class from a foreign markup input; handwritten code in
/// CheckedInCatalogView.Manual.cs extends the generated surface.
/// </summary>
public sealed partial class CheckedInCatalogView
{
    public string Title { get; set; } = string.Empty;

    public IReadOnlyList<string> Labels { get; set; } = Array.Empty<string>();

    public void Render()
    {
    }
}
