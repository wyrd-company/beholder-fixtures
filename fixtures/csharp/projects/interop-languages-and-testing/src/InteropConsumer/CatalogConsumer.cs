using Acme.InteropProducer;

namespace Acme.InteropConsumer;

public static class CatalogConsumer
{
    // Module/static consumption: F# module compiles to static class
    public static string ConsumeModuleStatic() => Catalog.formatLabel(42);

    // Class and static member consumption
    public static Widget ConsumeClass() => Widget.Create("sample", 3);
    public static Widget ConsumeClassWithDefault() => Widget.Create("sample");

    // Indexer / default-member consumption: Widget.Item, Container.Item
    public static string ConsumeWidgetIndexer()
    {
        var widget = new Widget("alpha", 1);
        return widget[2];
    }

    public static int ConsumeContainerIndexer()
    {
        var container = new Container(10);
        container[3] = 99;
        return container[3];
    }

    // Optional parameter consumption
    public static string ConsumeOptional() => new Widget("beta", 0).Describe();
    public static string ConsumeOptionalWithValue() => new Widget("beta", 0).Describe("note");
    public static string ConsumeOptionalViaString() => new Widget("gamma", 0).DescribeString();
    public static string ConsumeOptionalViaStringWithValue() => new Widget("gamma", 0).DescribeString("hello");

    // Functional metadata: F# function via System.Func
    public static int ConsumeFunctional() => Catalog.applyTransform(new System.Func<int, int>(x => x + 1), 5);
    public static int ConsumeFunctionalViaModule() => Catalog.applyTransform(Functional.asFunc, 5);

    // Type with no direct C# spelling: discriminated union Shape
    public static Shape ConsumeDiscriminatedUnion() => Shape.NewCircle(2.5);
    public static string DescribeShape(Shape shape)
    {
        if (shape.IsCircle)
        {
            return $"circle:{shape.Tag}";
        }

        if (shape.IsRectangle)
        {
            return "rect";
        }

        if (shape.IsPoint)
        {
            return "point";
        }

        return "unknown";
    }

    public static bool IsCircle(Shape shape) => shape.IsCircle;
    public static double CircleRadius(Shape shape) => shape is Shape.Circle c ? c.radius : -1;

    // Static property/member consumption
    public static Widget GetDefaultWidget() => Widget.DefaultWidget;
    public static Container GetEmptyContainer() => Container.Empty;

    // Direct call versus framework-mediated: this method is called directly
    public static int DirectCallExample() => Catalog.formatLabel(99).Length;
}
