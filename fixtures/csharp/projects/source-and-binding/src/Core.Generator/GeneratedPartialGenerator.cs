using Microsoft.CodeAnalysis;

namespace SourceBinding.Core.Generator;

[Generator]
public sealed class GeneratedPartialGenerator : IIncrementalGenerator
{
    public void Initialize(IncrementalGeneratorInitializationContext context)
    {
        context.RegisterPostInitializationOutput(ctx =>
        {
            const string source = """
                namespace SourceBinding.Core.Partial;

                public partial class GeneratedCatalog
                {
                    public int GeneratedValue => 42;

                    public string DescribeGenerated() => $"generated:{GeneratedValue}";

                    public string DescribeCombined() => $"{DescribeHandwritten()}+{DescribeGenerated()}";
                }
                """;
            ctx.AddSource("GeneratedCatalog.g.cs", source);
        });
    }
}
