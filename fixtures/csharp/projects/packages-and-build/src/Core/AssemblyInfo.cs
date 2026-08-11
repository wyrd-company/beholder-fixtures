// CS-CAN-014: handwritten assembly info contrast — SDK generates assembly attributes in obj/ (AssemblyTitle, Version, etc.); this file shows explicit non-conflicting metadata that coexists without duplication.
// Contrast auto-generated vs handwritten: SDK generates AssemblyInfo in obj/ (GenerateAssemblyInfo=true); handwritten attributes like AssemblyMetadata survive alongside.
using System.Reflection;

[assembly: AssemblyMetadata("FixturedBy", "packages-and-build")]
[assembly: AssemblyMetadata("Fixture", "packages-and-build-core")]
