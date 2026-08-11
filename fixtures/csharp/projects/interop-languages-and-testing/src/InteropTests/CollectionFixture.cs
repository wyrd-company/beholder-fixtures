using Xunit;

namespace Acme.InteropTests;

public sealed class SharedCollectionFixture : IDisposable
{
    public string Label => "shared";

    public void Dispose()
    {
    }
}

[CollectionDefinition("shared-collection")]
public sealed class SharedCollection : ICollectionFixture<SharedCollectionFixture>
{
}

[Collection("shared-collection")]
public sealed class CollectionTests
{
    private readonly SharedCollectionFixture _shared;

    public CollectionTests(SharedCollectionFixture shared)
    {
        _shared = shared;
    }

    [Fact]
    public void Collection_fixture_is_shared_across_tests()
    {
        Assert.Equal("shared", _shared.Label);
    }
}
