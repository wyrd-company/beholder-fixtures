namespace Bakery.TypesAndValues.Nullable.AnnotatedApi;

public enum StaleKind
{
    Plain = 0,
    Sourdough = 1,
    Rye = 2,
}

public static class StaleConstants
{
    public const StaleKind Favorite = StaleKind.Sourdough;

    public const int FavoriteValue = (int)StaleKind.Sourdough;
}
