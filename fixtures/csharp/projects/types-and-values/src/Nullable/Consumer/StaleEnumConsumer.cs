using Bakery.TypesAndValues.Nullable.AnnotatedApi;

namespace Bakery.TypesAndValues.Nullable.Consumer;

public static class StaleEnumConsumer
{
    public static StaleKind ConsumeFavorite() => StaleConstants.Favorite;

    public static int ConsumeFavoriteValue() => StaleConstants.FavoriteValue;

    public static bool VerifyEmbedded()
    {
        StaleKind kind = ConsumeFavorite();
        int value = ConsumeFavoriteValue();
        return kind == StaleKind.Sourdough && value == 1;
    }

    // The constant is embedded as a literal at the consumer call site;
    // rebuilding the producer with a different value would leave this
    // consumer stale until recompiled. Both producer and consumer are
    // project-local assemblies (AnnotatedApi producer, Consumer consumer).
}
