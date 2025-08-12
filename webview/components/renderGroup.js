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

import { renderBaseBlock } from './renderBaseBlock.js';
import { renderAutoResizableBody } from './renderAutoResizableBody.js';
import { renderComponent } from './renderComponent.js';
import { renderSection } from './renderSection.js';
import { LayoutManager } from '../core/layoutManager.js';

export function renderGroupGroup(container, groups, options = {}) {
  groups.forEach((group, idx) => {
    const path = options.pathPrefix ? `${options.pathPrefix}.groups[${idx}]` : `groups[${idx}]`;
    const block = renderGroup(group, { ...options, path });

    container.appendChild(block);
    options.renderBlock(block, 'group');
  });
}

export function renderGroup(group, options = {}) {
  const ns = group.namespace || '';

  const groupBox = renderBaseBlock({
    type: 'group',
    options: {
      ...options,
      events: group.events
    }
  });

  // Header
  const header = document.createElement('div');
  header.className = 'group-header';

  // Render additional sections
  const metaSections = [
    { key: 'namespace', icon: '🧭', label: 'Namespace', value: ns },
    { key: 'condition', icon: '❓', label: 'Condition', value: group.condition },
    { key: 'parameters', icon: '⚙️', label: 'Params', value: group.parameters }
  ];

  metaSections.forEach(({ key, icon, label, value }) => {
    if (value) {
      const section = renderSection(key, icon, label, value, {
        includeLeftPort: true,
        portIdPrefix: options.path,
        portRegistry: options.portRegistry
      });
      header.appendChild(section);
    }
  });

  groupBox.append(header);

  // Body
  const body = document.createElement('div');
  body.className = 'group-body';
  groupBox.appendChild(body);

  const innerLayoutManager = new LayoutManager(20, 40, 80, 40);
  const childOptions = {
    ...options,
    stopPropagation: true,
    constrainToParent: true,
    pathPrefix: `${options.path}.actions`,
    renderBlock: (block, columnType) => {
      requestAnimationFrame(() => {
        innerLayoutManager.placeBlock(block, columnType);
      });
    }
  };

  const actions = group.actions || {};
  for (const [key, value] of Object.entries(actions)) {
    renderComponent({ type: key, value: value, namespace: ns }, body, childOptions);
  }

  renderAutoResizableBody(groupBox, 'block', ['.group-header']);

  return groupBox;
}
