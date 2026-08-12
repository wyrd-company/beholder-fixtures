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

            var root = tree.GetRoot(context.CancellationToken);
            var node = root.FindNode(diagnostic.Location.SourceSpan);
            var model = context.GetSemanticModel(tree);
            var declared = node as Microsoft.CodeAnalysis.CSharp.Syntax.TypeDeclarationSyntax;
            Microsoft.CodeAnalysis.ISymbol? symbol = null;
            if (declared != null)
            {
                symbol = model.GetDeclaredSymbol(declared, context.CancellationToken);
            }
            else
            {
                symbol = model.GetSymbolInfo(node, context.CancellationToken).Symbol
                    ?? model.GetDeclaredSymbol(node, context.CancellationToken);
            }

            if (symbol is null)
            {
                continue;
            }

            var target = symbol is Microsoft.CodeAnalysis.INamedTypeSymbol nt ? (Microsoft.CodeAnalysis.ISymbol)nt : symbol;
            if (target is Microsoft.CodeAnalysis.INamedTypeSymbol named)
            {
                target = named;
            }

            foreach (var attr in target.GetAttributes())
            {
                var name = attr.AttributeClass?.Name;
                if (name == "SuppressCatalogNamingAttribute" || name == "GeneratedCodeAttribute")
                {
                    context.ReportSuppression(Suppression.Create(Descriptor, diagnostic));
                    break;
                }
            }
        }
    }
}
