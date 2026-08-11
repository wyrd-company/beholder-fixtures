/// <amd-module name="legacy-amd-named-second" />
/// <amd-dependency path="legacy-amd-side-effect" />

// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import { amdModuleOrder } from "./module-first";

export var amdModuleSuffix = amdModuleOrder + "-second";
