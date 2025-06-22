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

import { renderArguments } from './render/renderArguments.js';
import { renderNodeGroup } from './render/renderNode.js';
import { renderIncludesGroup } from './render/renderInclude.js';
import { renderGroup } from './render/renderGroup.js';
import { renderEdges } from './render/renderEdges.js';
import { enableZoomAndPan } from './zoomPanController.js';
import { renderComposableGroup } from './render/renderComposableGroup.js';

const argumentRegistry = {};
const blockRegistry = {};
const portRegistry = {};

window.addEventListener('message', (event) => {
    const message = event.data;
    if (message.type == 'launchmap-data') {
        renderAll(message.data);
    }
});

function renderAll(data) {
    const editor = document.getElementById("editor");
    editor.innerHTML = "";

    // Create zoom layer
    const zoomLayer = document.createElement("div");
    zoomLayer.id = "zoom-layer";
    editor.appendChild(zoomLayer);

    // Edges
    const edgeLayer = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    edgeLayer.setAttribute("id", "edge-layer");
    edgeLayer.classList.add("edge-layer");
    zoomLayer.appendChild(edgeLayer);

    // Graph Nodes
    const layoutCtx = { x: 100, y: 100 };

    // Top Level nodes and includes
    renderArguments(zoomLayer, data.arguments || [], layoutCtx, 
        { argumentRegistry, blockRegistry, portRegistry, parsedData: data, renderEdges });
    renderNodeGroup(zoomLayer, data.nodes || [], "", layoutCtx, 
        { pathPrefix: "nodes", blockRegistry, argumentRegistry, portRegistry, parsedData: data, renderEdges});
    renderIncludesGroup(zoomLayer, data.includes || [], "", layoutCtx, 
        { pathPrefix: "includes", blockRegistry, argumentRegistry, portRegistry, parsedData: data, renderEdges });

    // Recursively render groups
    (data.groups || []).forEach((group, idx) => {
        renderGroup(group, `groups[${idx}]`, zoomLayer, layoutCtx, 
            { path: `groups[${idx}]`, blockRegistry, argumentRegistry, portRegistry, parsedData: data, renderEdges });
    });

    // Composable nodes
    (data.composable_nodes || []).forEach((group, idx) => {
        renderComposableGroup(group, `composable_nodes[${idx}]`, zoomLayer, layoutCtx,
            { path: `composable_nodes[${idx}]`, blockRegistry, argumentRegistry, portRegistry, parsedData: data, renderEdges });
    });

    renderEdges(data, portRegistry);
    enableZoomAndPan(editor, zoomLayer, () => renderEdges(data, portRegistry));
}