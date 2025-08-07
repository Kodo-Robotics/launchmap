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

export function getWebviewHtml(
  webview: vscode.Webview,
  extensionUri: vscode.Uri
): string {
  const scriptUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, "webview", "script.js")
  );
  const styleUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, "webview", "style.css")
  );
  const logoUri = webview.asWebviewUri(
    vscode.Uri.joinPath(extensionUri, "assets", "launchmap-logo.png")
  );
  let announcement = {
    text: "🚀 LaunchMap Discord Server is live — ",
    click: "Join us now",
    link: "https://discord.com/invite/38DvuSUn",
  };

  return `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource} https:; script-src 'unsafe-inline' 'unsafe-eval' ${webview.cspSource}; style-src ${webview.cspSource};">
            <link href="${styleUri}" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=League+Spartan&display=swap" rel="stylesheet">

        </head>
        <body>
          <div id="header">
          <div id="announcement">
              <p>${announcement.text} <a href="${announcement.link}" target="_blank">${announcement.click}</a></p>
              <button>❌</button>
          </div>
              <button id="export-btn">💾 Export JSON</button>
          </div>
            <div id="editor">
            </div>
            <div id="watermark">
            <img src="${logoUri}" alt="Logo" />
            <p>LaunchMap</p>
            </div>
            <script src="${scriptUri}" type="module"></script>
        </body>
        </html>
    `;
}
