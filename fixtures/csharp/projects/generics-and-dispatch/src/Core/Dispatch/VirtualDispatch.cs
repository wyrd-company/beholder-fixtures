namespace GenericsAndDispatch.Core.Dispatch;

public abstract class ShapeBase
{
    public abstract string Kind { get; }
    public abstract double Area();
    public virtual string Describe() => $"shape:{Kind}";
    public virtual ShapeBase Clone() => this;
}

public class Polygon : ShapeBase
{
    public int Sides { get; init; }
    public Polygon(int sides) => Sides = sides;
    public override string Kind => $"polygon-{Sides}";
    public override double Area() => Sides * 10;
    public override Polygon Clone() => new(Sides);
    public virtual string Tag() => "polygon";
}

public class Quadrilateral : Polygon
{
    public double Width { get; init; }
    public double Height { get; init; }
    public Quadrilateral(double width, double height) : base(4) => (Width, Height) = (width, height);
    public override string Kind => "quadrilateral";
    public override double Area() => Width * Height;
    public sealed override Polygon Clone() => new Quadrilateral(Width, Height);
    public override string Tag() => "quad";
    public virtual Quadrilateral Scale(double factor) => new(Width * factor, Height * factor);
}

public sealed class Square : Quadrilateral
{
    public Square(double side) : base(side, side) { }
    public override string Kind => "square";
    public override double Area() => Width * Width;
    // Sealed clone cannot be overridden further; covariant return earlier preserved runtime slot identity.
    public new Square Scale(double factor) => new(Width * factor);
    public override string Describe() => $"square:{Width}";
}

// New virtual creates a separate slot.
public class BaseWithNewVirtual
{
    public virtual string Identify() => "base";
}

public class DerivedWithNewVirtual : BaseWithNewVirtual
{
    public new virtual string Identify() => "derived-new";
}

public class FurtherDerived : DerivedWithNewVirtual
{
    public override string Identify() => "further";
}

// Virtual call during construction pattern (avoid heavy work, just record).
public abstract class ConstructionBase
{
    protected ConstructionBase() => Captured = Describe();
    public string Captured { get; }
    public abstract string Describe();
}

public sealed class ConstructionDerived : ConstructionBase
{
    private readonly string _hint;
    public ConstructionDerived(string hint) => _hint = hint;
    public override string Describe() => $"derived:{_hint}";
}

// Re-abstraction.
public abstract class AbstractProcessor : ShapeBase
{
    public abstract override double Area();
}

public sealed class ConcreteProcessor : AbstractProcessor
{
    public override string Kind => "concrete";
    public override double Area() => 42;
}

public static class VirtualDispatchExercises
{
    public static void Run()
    {
        ShapeBase[] shapes = [new Polygon(3), new Quadrilateral(3, 4), new Square(5)];
        foreach (var shape in shapes)
        {
            string kind = shape.Kind;
            double area = shape.Area();
            string described = shape.Describe();
            ShapeBase cloned = shape.Clone();
            _ = kind; _ = area; _ = described; _ = cloned;
        }

        // Calls through several static types and base-qualified.
        Quadrilateral quad = new(2, 5);
        Polygon asPolygon = quad;
        ShapeBase asShape = quad;
        string viaQuad = quad.Tag();
        string viaPolygon = asPolygon.Tag();
        string viaBase = quad.Describe();

        // Base-qualified call.
        var square = new Square(3);
        string baseDescribe = ((Quadrilateral)square).Describe();

        // Sealed override and covariant return verified via compile-time and runtime.
        Polygon clonedQuad = quad.Clone();

        // New virtual separate slot.
        BaseWithNewVirtual baseRef = new DerivedWithNewVirtual();
        string identifyBase = baseRef.Identify();
        DerivedWithNewVirtual derivedRef = new FurtherDerived();
        string identifyDerived = derivedRef.Identify();

        // Virtual during construction.
        var construction = new ConstructionDerived("hint");
        _ = construction.Captured;

        // Re-abstraction completeness.
        AbstractProcessor processor = new ConcreteProcessor();
        double processorArea = processor.Area();

        _ = viaQuad; _ = viaPolygon; _ = viaBase; _ = baseDescribe;
        _ = clonedQuad; _ = identifyBase; _ = identifyDerived; _ = processorArea;
    }
}
