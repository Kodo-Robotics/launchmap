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

export function renderNodeGroup(container, nodes, options={}) {
  nodes.forEach((node, idx) => {
    const path = options.pathPrefix ? `${options.pathPrefix}.nodes[${idx}]` : `nodes[${idx}]`;
    const block = renderNode(node, { ...options, path });

    container.appendChild(block);
    options.renderBlock(block, 'node');
  });
}

function renderNode(node, options) {
  const block = renderBaseBlock({
    type: 'node',
    options: {
      ...options,
      events: node.events
    }
  });

  // Node name
  const titleLabel = node.name || node.executable || '(anonymous)';

  // Sections
  const renderOptions = { includeLeftPort: true, portIdPrefix: options.path, portRegistry: options.portRegistry };
  block.appendChild(renderSection('name', '📛', 'Name', titleLabel, renderOptions));
  block.appendChild(renderSection('package', '📦', 'Package', node.package, renderOptions));
  block.appendChild(renderSection('executable', '▶️', 'Executable', node.executable, renderOptions));
  block.appendChild(renderSection('output', '🖥️', 'Output', node.output || '—', renderOptions));

  // Render additional sections
  const metaSections = [
    { key: 'condition', icon: '❓', label: 'Condition', value: node.condition },
    { key: 'parameters', icon: '⚙️', label: 'Params', value: node.parameters },
    { key: 'arguments', icon: '💬', label: 'Args', value: node.arguments },
    { key: 'env', icon: '🌍', label: 'Environment Variables', value: node.env }
  ];

  metaSections.forEach(({ key, icon, label, value }) => {
    if (value) {
      const section = renderSection(key, icon, label, value, renderOptions);
      block.appendChild(section);
    }
  });

  return block;
}
