namespace Acme.InteropTests;

public sealed class SampleFixture : IDisposable
{
    public int Seed { get; } = 42;

    public void Dispose()
    {
    }
}
