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
import { setPluginDir } from '../utils/launchmapConfig';
import { updatePluginDirStatusBar } from '../ui/pluginDirStatusBar';

export function registerSetPluginDir(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('launchmap.setPluginDir', async () => {
            const selected = await vscode.window.showOpenDialog({
                canSelectFiles: false,
                canSelectFolders: true,
                canSelectMany: false,
                openLabel: 'Select Plugin Directory'
            });

            if (!selected || selected.length === 0) return;

            const pluginPath = selected[0].fsPath;
            await setPluginDir(pluginPath);
            await updatePluginDirStatusBar();
        })
    );
}