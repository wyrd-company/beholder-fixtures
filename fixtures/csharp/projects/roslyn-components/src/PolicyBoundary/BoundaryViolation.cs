namespace Fixture.Roslyn.PolicyBoundary.Catalog;

// CS-CAN-102: one physical source compiled under two policy configurations.
//
// This is a public catalog participant (its namespace marks it as part of the
// catalog model) whose name does not carry the required "Catalog" suffix, so the
// CS-CAN-016 analyzer reports RCAN001 against it. PolicyBoundary.csproj compiles
// this single file two ways:
//
//   * Strict  - <WarningsAsErrors>RCAN001</WarningsAsErrors> promotes RCAN001 to
//               an error, so the build fails on this same source.
//   * Relaxed - <NoWarn>RCAN001</NoWarn> silences RCAN001, so the build passes on
//               this same source.
//
// Same source, opposite outcome, selected purely by build configuration.
public class BoundaryViolation
{
    public string Tag { get; set; } = string.Empty;
}
