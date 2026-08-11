/**
 * Compiler-API transformer surface (TS-CAN-090).
 * Uses the pinned `typescript` package as a before transformer.
 * Demonstrates a synthetic node without source position and a
 * generated runtime edge absent from source.
 */

import * as ts from "typescript";
import * as fs from "node:fs";

const sourcePath = "src/transform-source.ts";
const sourceText = fs.readFileSync(sourcePath, "utf8");

function createExampleTransformer(): ts.TransformerFactory<ts.SourceFile> {
  return (context) => {
    const factory = context.factory;
    return (sourceFile) => {
      // synthetic node without source position: string literal with pos -1
      const syntheticLiteral = factory.createStringLiteral("synthetic-node");
      ts.setTextRange(syntheticLiteral, { pos: -1, end: -1 });

      // generated runtime edge absent from source: inject `export const __generatedRuntimeEdge = "synthetic-node"`
      const injected = factory.createVariableStatement(
        [factory.createModifier(ts.SyntaxKind.ExportKeyword)],
        factory.createVariableDeclarationList(
          [
            factory.createVariableDeclaration(
              factory.createIdentifier("__generatedRuntimeEdge"),
              undefined,
              undefined,
              syntheticLiteral,
            ),
          ],
          ts.NodeFlags.Const,
        ),
      );

      // mark injected statement as synthetic (no original pos)
      ts.setTextRange(injected, { pos: -1, end: -1 });

      const updated = factory.updateSourceFile(sourceFile, [
        ...sourceFile.statements,
        injected,
      ]);

      return updated;
    };
  };
}

const sourceFile = ts.createSourceFile(
  sourcePath,
  sourceText,
  ts.ScriptTarget.ES2022,
  true,
  ts.ScriptKind.TS,
);

const result = ts.transform(sourceFile, [createExampleTransformer()]);
const transformed = result.transformed[0] as ts.SourceFile;
const printer = ts.createPrinter({ newLine: ts.NewLineKind.LineFeed });
const output = printer.printFile(transformed);

console.log(`// compiler-API before transformer on ${sourcePath}`);
console.log(output);
console.log(
  "// injected `__generatedRuntimeEdge` is a generated runtime edge absent from source",
);
console.log(
  "// its initializer `synthetic-node` has no source position (pos -1)",
);

// verify synthetic position
const injectedStmt = transformed.statements[transformed.statements.length - 1];
const pos = (injectedStmt as unknown as { pos: number }).pos;
if (pos !== -1) {
  // transformer keeps synthetic range on literal; statement may have pos but literal is synthetic
  const literal = (injectedStmt as ts.VariableStatement).declarationList
    .declarations[0].initializer;
  const litPos = (literal as unknown as { pos: number }).pos;
  if (litPos !== -1) {
    console.error("expected synthetic node to have pos -1");
    process.exit(1);
  }
}

result.dispose();
