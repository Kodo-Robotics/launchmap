// Copyright (c) 2025 Kodo Robotics
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import * as vscode from "vscode";
import { registerOpenVisualizer } from "./commands/openVisualizer";
import { registerExportJson } from "./commands/exportJson";
import { registerImportJson } from "./commands/importJson";
import { registerSetPluginDir } from "./commands/setPluginDir";
import { initPluginDirStatusBar } from "./ui/pluginDirStatusBar";

export function activate(context: vscode.ExtensionContext) {
  registerOpenVisualizer(context);
  registerExportJson(context);
  registerImportJson(context);
  registerSetPluginDir(context);

  initPluginDirStatusBar();
}
