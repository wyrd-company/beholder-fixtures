namespace SourceBinding.Core.Partial;

public partial struct GridPoint
{
    public int X;
    public int Y;
}

public partial struct GridPoint
{
    public int Sum() => X + Y;

    public static GridPoint Origin => new GridPoint { X = 0, Y = 0 };
}
