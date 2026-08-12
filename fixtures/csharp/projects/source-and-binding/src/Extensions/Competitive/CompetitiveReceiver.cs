namespace SourceBinding.Extensions.Competitive;

public sealed class CompetitiveReceiver
{
    public int GetValue() => 1;
}

public static class CompetitiveReceiverExtensions
{
    public static int GetValue(this CompetitiveReceiver receiver) => 2;
}
