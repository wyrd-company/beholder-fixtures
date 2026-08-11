using System.Collections.Immutable;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Diagnostics;

namespace Fixture.Roslyn.Analyzer;

/// <summary>
/// Analyzer for CS-CAN-016: inspects semantic state (type declaration)
/// without changing emitted program semantics. Reports when a public type
/// does not carry a "Catalog" suffix, as a lightweight naming policy.
/// Respects generated-code configuration via <see cref="GeneratedCodeAnalysisFlags.None"/>.
/// </summary>
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class CatalogNamingAnalyzer : DiagnosticAnalyzer
{
    public const string DiagnosticId = "RCAN001";

    private static readonly DiagnosticDescriptor Rule = new(
        id: DiagnosticId,
        title: "Public catalog type should use Catalog suffix",
        messageFormat: "Type '{0}' should end with 'Catalog' to satisfy the catalog naming policy",
        category: "RoslynComponents.Naming",
        defaultSeverity: DiagnosticSeverity.Warning,
        isEnabledByDefault: true,
        description: "Public types that participate in the catalog model are expected to use a Catalog suffix.");

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics => ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext context)
    {
        // Generated-code treatment: do not analyze generated files.
        context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
        context.EnableConcurrentExecution();

        context.RegisterSymbolAction(AnalyzeSymbol, SymbolKind.NamedType);
    }

    private static void AnalyzeSymbol(SymbolAnalysisContext context)
    {
        var symbol = (INamedTypeSymbol)context.Symbol;

        // Only analyze public, non-generated type declarations in source.
        if (symbol.DeclaredAccessibility != Accessibility.Public)
        {
            return;
        }

        if (symbol.IsImplicitlyDeclared)
        {
            return;
        }

        // Limit to class/record declarations (not interfaces, enums, delegates).
        if (symbol.TypeKind != TypeKind.Class)
        {
            return;
        }

        if (symbol.Name.EndsWith("Catalog", System.StringComparison.Ordinal))
        {
            return;
        }

        // Inspect semantic state: if the type is marked with GenerateCatalog or lives
        // in a namespace containing "Catalog", consider it a catalog participant.
        var hasGenerateAttribute = false;
        foreach (var attr in symbol.GetAttributes())
        {
            if (attr.AttributeClass?.Name == "GenerateCatalogAttribute")
            {
                hasGenerateAttribute = true;
                break;
            }
        }

        var inCatalogNamespace = symbol.ContainingNamespace.ToDisplayString().Contains("Catalog");

        if (!hasGenerateAttribute && !inCatalogNamespace)
        {
            return;
        }

        // Only flag locations that are in source (not metadata).
        foreach (var location in symbol.Locations)
        {
            if (location.IsInSource)
            {
                var diagnostic = Diagnostic.Create(Rule, location, symbol.Name);
                context.ReportDiagnostic(diagnostic);
                break;
            }
        }
    }
}
