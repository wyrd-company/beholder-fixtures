using System;
using System.Linq;
using System.Text;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Text;

namespace Fixture.Roslyn.Generator;

/// <summary>
/// Incremental generator that demonstrates every generator input described by
/// CS-CAN-015: syntax, symbols, <c>AdditionalFiles</c>, analyzer config, and
/// metadata, and that emits a partial counterpart plus a diagnostic while
/// recording its own provenance in the emitted source.
/// </summary>
[Generator]
public sealed class CatalogGenerator : IIncrementalGenerator
{
    private const string GenerateCatalogAttributeName = "Fixture.Roslyn.Generator.GenerateCatalogAttribute";
    private const string DiagnosticId = "RCGEN001";

    private static readonly DiagnosticDescriptor GeneratedDiagnostic = new(
        id: DiagnosticId,
        title: "Catalog entry generated",
        messageFormat: "Catalog '{0}' was generated from '{1}' (hint: {2})",
        category: "RoslynComponents",
        defaultSeverity: DiagnosticSeverity.Warning,
        isEnabledByDefault: true,
        description: "Emitted by the incremental catalog generator after producing its counterpart.");

    public void Initialize(IncrementalGeneratorInitializationContext context)
    {
        // Symbol input via ForAttributeWithMetadataName plus syntax broad check.
        var attributedClasses = context.SyntaxProvider.ForAttributeWithMetadataName(
            fullyQualifiedMetadataName: GenerateCatalogAttributeName,
            predicate: static (node, _) => node is ClassDeclarationSyntax,
            transform: static (ctx, _) => new AttributedClass(
                (INamedTypeSymbol)ctx.TargetSymbol,
                (ClassDeclarationSyntax)ctx.TargetNode,
                GetCatalogName(ctx)));

        // AdditionalFiles input.
        var additionalFiles = context.AdditionalTextsProvider
            .Where(static text => text.Path.EndsWith("generation-config.txt", StringComparison.OrdinalIgnoreCase)
                               || text.Path.EndsWith(".additional.txt", StringComparison.OrdinalIgnoreCase))
            .Collect();

        // Analyzer config + metadata + syntax inputs combined.
        var inputs = attributedClasses
            .Combine(additionalFiles)
            .Combine(context.AnalyzerConfigOptionsProvider)
            .Combine(context.CompilationProvider.Select(static (c, _) => c.GetTypeByMetadataName("System.Collections.Generic.List`1") != null))
            .Combine(context.SyntaxProvider.CreateSyntaxProvider(
                predicate: static (node, _) => node is ClassDeclarationSyntax cds && cds.AttributeLists.Count > 0,
                transform: static (ctx, _) => (ClassDeclarationSyntax)ctx.Node).Collect());

        context.RegisterSourceOutput(inputs, (ctx, tuple) =>
        {
            // Unwrap: (((AttributedClass + AdditionalFiles) + AnalyzerConfigOptionsProvider) + bool) + syntax
            var inner = tuple.Left; // ((AttributedClass, AdditionalFiles), AnalyzerConfig, bool)
            var allClasses = tuple.Right; // syntax collection
            var mid = inner.Left; // (AttributedClass, AdditionalFiles), AnalyzerConfig
            var hasListMetadata = inner.Right;
            var attributedClass = mid.Left.Left;
            var files = mid.Left.Right;
            var optionsProvider = mid.Right;

            var symbol = attributedClass.Symbol;
            var catalogName = attributedClass.CatalogName ?? symbol.Name;

            var globalOptions = optionsProvider.GlobalOptions;
            globalOptions.TryGetValue("build_property.GeneratorProvenance", out var provenance);
            provenance ??= "roslyn-components-generator";

            var sourceFile = attributedClass.Syntax.SyntaxTree.FilePath;
            var fileOptions = optionsProvider.GetOptions(attributedClass.Syntax.SyntaxTree);
            if (fileOptions.TryGetValue("build_property.DisableCatalogGeneration", out var disable) &&
                disable.Equals("true", StringComparison.OrdinalIgnoreCase))
            {
                return;
            }

            fileOptions.TryGetValue("build_property.CatalogPrefix", out var prefix);
            prefix ??= string.Empty;

            var rawAdditional = string.Join("; ", files.Select(f => f.GetText()?.ToString()?.Trim() ?? string.Empty).Where(s => s.Length > 0));
            var additionalContent = rawAdditional.Replace("\r", " ").Replace("\n", " ");
            if (additionalContent.Length == 0)
            {
                additionalContent = "(no additional files)";
            }

            var metadataNote = hasListMetadata ? "List<T> available" : "List<T> unavailable";
            var classCount = allClasses.Length;

            var ns = symbol.ContainingNamespace.IsGlobalNamespace
                ? string.Empty
                : symbol.ContainingNamespace.ToDisplayString();
            var className = symbol.Name;
            var fullCatalogName = string.IsNullOrEmpty(prefix) ? catalogName : prefix + catalogName;
            var hintName = (string.IsNullOrEmpty(ns) ? string.Empty : ns.Replace('.', '_') + "_") + className + ".Catalog.g.cs";

            var source = BuildPartialSource(ns, className, fullCatalogName, provenance, additionalContent, metadataNote, classCount, hintName, sourceFile);
            ctx.AddSource(hintName, SourceText.From(source, Encoding.UTF8));

            var diagnostic = Diagnostic.Create(GeneratedDiagnostic, attributedClass.Syntax.GetLocation(), fullCatalogName, sourceFile, hintName);
            ctx.ReportDiagnostic(diagnostic);
        });
    }

    private static string? GetCatalogName(GeneratorAttributeSyntaxContext ctx)
    {
        if (ctx.Attributes.Length == 0)
        {
            return ctx.TargetSymbol.Name;
        }

        var attr = ctx.Attributes[0];
        if (attr.ConstructorArguments.Length > 0 && attr.ConstructorArguments[0].Value is string s && s.Length > 0)
        {
            return s;
        }

        foreach (var kv in attr.NamedArguments)
        {
            if (kv.Key == "CatalogName" && kv.Value.Value is string ns && ns.Length > 0)
            {
                return ns;
            }
        }

        return ctx.TargetSymbol.Name;
    }

    private static string BuildPartialSource(
        string ns,
        string className,
        string catalogName,
        string provenance,
        string additionalContent,
        string metadataNote,
        int classCount,
        string hintName,
        string sourceFile)
    {
        var nsOpen = string.IsNullOrEmpty(ns) ? string.Empty : "namespace " + ns + "\n{\n";
        var nsClose = string.IsNullOrEmpty(ns) ? string.Empty : "}\n";

        return
            "// <auto-generated/>\n" +
            "// Provenance: " + provenance + "\n" +
            "// Generator: Fixture.Roslyn.Generator.CatalogGenerator\n" +
            "// HintName: " + hintName + "\n" +
            "// SourceFile: " + sourceFile + "\n" +
            "// AdditionalFiles: " + additionalContent + "\n" +
            "// Metadata: " + metadataNote + "\n" +
            "// SyntaxClassCount: " + classCount + "\n" +
            "#nullable enable\n" +
            nsOpen +
            "    partial class " + className + "\n" +
            "    {\n" +
            "        public string CatalogName => \"" + catalogName + "\";\n" +
            "        public string GeneratorProvenance => \"" + provenance + "\";\n" +
            "        public string GeneratedHintName => \"" + hintName + "\";\n" +
            "        public string DescribeCatalog() => $\"Catalog '{CatalogName}' via '{GeneratorProvenance}' (hint {GeneratedHintName})\";\n" +
            "    }\n" +
            nsClose;
    }

    private sealed class AttributedClass
    {
        public AttributedClass(INamedTypeSymbol symbol, ClassDeclarationSyntax syntax, string? catalogName)
        {
            Symbol = symbol;
            Syntax = syntax;
            CatalogName = catalogName;
        }

        public INamedTypeSymbol Symbol { get; }
        public ClassDeclarationSyntax Syntax { get; }
        public string? CatalogName { get; }
    }
}
