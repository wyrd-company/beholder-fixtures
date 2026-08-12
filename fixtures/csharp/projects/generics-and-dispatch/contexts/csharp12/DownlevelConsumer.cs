using GenericsAndDispatch.CSharp13;

namespace GenericsAndDispatch.CSharp12;

public static class DownlevelConsumer
{
    public static int ConsumeRegular()
    {
        var regular = new RegularValue(41);
        return AllowsRefStructAlgorithm.Run(regular);
    }

    public static int ConsumeTransformed()
    {
        var regular = new RegularValue(21);
        return AllowsRefStructAlgorithm.RunWithTransform(regular, static v => v * 2);
    }

    public static void Run()
    {
        int a = ConsumeRegular();
        int b = ConsumeTransformed();
        _ = a; _ = b;
    }
}
