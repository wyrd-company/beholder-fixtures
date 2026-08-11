using Acme.InteropConsumer;
using Xunit;

namespace Acme.InteropTests;

public sealed class DiscoveryTests : IClassFixture<SampleFixture>, IDisposable
{
    private readonly SampleFixture _fixture;
    private bool _disposed;

    public DiscoveryTests(SampleFixture fixture)
    {
        _fixture = fixture;
    }

    public static IEnumerable<object[]> LabeledCases =>
    [
        [1, "item:1"],
        [2, "item:2"],
    ];

    public static IEnumerable<object[]> NamedMemberData => LabeledCases;

    [Fact]
    public void Fact_ordinary_test_discovered_by_attribute()
    {
        Assert.Equal("item:42", CatalogConsumer.ConsumeModuleStatic());
    }

    [Theory]
    [InlineData(1, "item:1")]
    [InlineData(2, "item:2")]
    public void Theory_inline_data_driven(int input, string expected)
    {
        Assert.Equal(expected, Acme.InteropProducer.Catalog.formatLabel(input));
    }

    [Theory]
    [MemberData(nameof(NamedMemberData))]
    public void Theory_member_data_via_nameof(int input, string expected)
    {
        Assert.Equal(expected, Acme.InteropProducer.Catalog.formatLabel(input));
    }

    [Fact]
    public void Fact_fixture_lifecycle_constructs_via_constructor()
    {
        Assert.Equal(42, _fixture.Seed);
    }

    [Fact]
    public void Fact_consumer_still_callable_directly_contrasted_with_runner()
    {
        // Direct call (explicit invocation) versus framework-mediated discovery:
        // this assertion exercises the same consumer logic that the other tests
        // reach only when the VSTest host discovers and invokes them via
        // xunit.runner.visualstudio + Microsoft.NET.Test.Sdk.
        var result = CatalogConsumer.ConsumeFunctional();
        Assert.Equal(6, result);
    }

    public void Dispose()
    {
        if (!_disposed)
        {
            _disposed = true;
        }
    }
}
