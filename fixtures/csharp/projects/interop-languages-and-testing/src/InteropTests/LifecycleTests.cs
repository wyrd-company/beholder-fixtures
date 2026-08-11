using Xunit;

namespace Acme.InteropTests;

public sealed class LifecycleTests : IAsyncLifetime
{
    private int _value;

    public Task InitializeAsync()
    {
        _value = 10;
        return Task.CompletedTask;
    }

    public Task DisposeAsync()
    {
        _value = 0;
        return Task.CompletedTask;
    }

    [Fact]
    public void Async_lifecycle_initializes_before_test()
    {
        Assert.Equal(10, _value);
    }

    [Theory]
    [InlineData(3, 30)]
    [InlineData(4, 40)]
    public void Data_driven_with_async_lifecycle(int input, int expected)
    {
        Assert.Equal(expected, input * _value / 10 * 10);
    }
}
