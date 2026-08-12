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

    // Unattributed, test-shaped probe — NOT discovered by xUnit (no [Fact]/[Theory])
    // Used to contrast explicit direct invocation with framework-mediated discovery.
    private sealed class UnattributedProbe
    {
        public void Probe_without_attribute()
        {
            // Test-shaped: contains an assertion, but no attribute so runner never discovers it.
            Assert.Equal(6, CatalogConsumer.ConsumeFunctional());
        }
    }

    [Fact]
    public void Fact_direct_invocation_of_unattributed_test_shape()
    {
        // Contrast: explicit, direct invocation of an unattributed test-shaped method.
        // This path is NOT framework-discovered; the runner discovers only the
        // surrounding [Fact], which then calls the probe directly via `new`.
        new UnattributedProbe().Probe_without_attribute();
    }

    public void Dispose()
    {
        if (!_disposed)
        {
            _disposed = true;
        }
    }
}
