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

import { renderSection } from './renderSection.js';
import { renderBaseBlock } from './renderBaseBlock.js';

export function renderComposableNodeGroup(container, nodes, namespace, layoutCtx, options={}) {
    nodes.forEach((node, idx) => {
        const path = options.pathPrefix ? `${options.pathPrefix}.composable_nodes[${idx}]` : `composable_nodes[${idx}]`;
        const block = renderComposableNode(node, namespace, layoutCtx, { ...options, path });
        container.appendChild(block);
        layoutCtx.y += 100;
    });

    layoutCtx.x += 250;
    layoutCtx.y = 100;
}

function renderComposableNode(node, namespace, layoutCtx, options) {
    const block = renderBaseBlock({
        type: 'composable-node',
        layoutCtx,
        options: {
            ...options,
            events: node.events
        }
    })

    // Node name
    const titleLabel = node.name || node.plugin || "(anonymous)";
    const fullName = namespace ? `${namespace}/${titleLabel}` : titleLabel;

    // Sections
    const renderOptions = { includeLeftPort: true, portIdPrefix: options.path, portRegistry: options.portRegistry };
    block.appendChild(renderSection("name", "📛", "Name", fullName, renderOptions));
    block.appendChild(renderSection("package", "📦", "Package", node.package, renderOptions));
    block.appendChild(renderSection("plugin", "🔌", "Plugin", node.plugin, renderOptions));

    if (node.parameters?.length > 0) {
        block.appendChild(renderSection("parameters", "⚙️", "Params", node.parameters, renderOptions));
    }

    if (node.arguments?.length > 0) {
        block.appendChild(renderSection("arguments", "💬", "Args", node.arguments, renderOptions));
    }

    return block;
}