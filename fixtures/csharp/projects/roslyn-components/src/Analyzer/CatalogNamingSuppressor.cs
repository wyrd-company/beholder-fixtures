using System.Collections.Immutable;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Diagnostics;

namespace Fixture.Roslyn.Analyzer;

/// <summary>
/// Suppressor for CS-CAN-016 and CS-CAN-102 precedence: suppresses
/// <c>RCAN001</c> when the target type is annotated with
/// <see cref="SuppressCatalogNamingAttribute"/> or carries <c>GeneratedCodeAttribute</c>.
/// Demonstrates suppression precedence over analyzer severity.
/// </summary>
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class CatalogNamingSuppressor : DiagnosticSuppressor
{
    private static readonly SuppressionDescriptor Descriptor = new(
        id: "RCSUP001",
        suppressedDiagnosticId: CatalogNamingAnalyzer.DiagnosticId,
        justification: "Suppressed by SuppressCatalogNamingAttribute or generated-code provenance.");

    public override ImmutableArray<SuppressionDescriptor> SupportedSuppressions => ImmutableArray.Create(Descriptor);

    public override void ReportSuppressions(SuppressionAnalysisContext context)
    {
        foreach (var diagnostic in context.ReportedDiagnostics)
        {
            if (diagnostic.Id != CatalogNamingAnalyzer.DiagnosticId)
            {
                continue;
            }

            var tree = diagnostic.Location.SourceTree;
            if (tree is null)
            {
                continue;
            }

            // Inspect the source text of the file for the suppression marker.
            // A production suppressor would resolve the symbol via the semantic model;
            // for this fixture the text check demonstrates the precedence hook
            // while keeping the analyzer assembly netstandard2.0-clean.
            var text = tree.GetText(context.CancellationToken).ToString();
            if (text.Contains("SuppressCatalogNaming") || text.Contains("GeneratedCode"))
            {
                context.ReportSuppression(Suppression.Create(Descriptor, diagnostic));
            }
        }
    }
}
