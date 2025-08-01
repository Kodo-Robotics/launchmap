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

import * as vscode from 'vscode';
import * as path from 'path';
import { runPythonParser } from '../python/runParser';
import { createVisualizerPanel } from '../panel/createVisualizerPanel';

let lastParsedData: any = null;

export function registerOpenVisualizer(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('launchmap.openVisualizer', async() => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showErrorMessage("No active editor with a launch file.");
                return;
            }

            const filePath = editor.document.fileName;
            const fileName = path.basename(filePath);
            const result = await runPythonParser(filePath);

            lastParsedData = JSON.parse(result);
            createVisualizerPanel(context, lastParsedData, fileName);
        })
    );
}

export function getLastParsedData() {
    return lastParsedData;
}

export function setLastParsedData(data: any) {
    lastParsedData = data;
}