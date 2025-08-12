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

export function renderComposableContainerGroup(container, groups, options = {}) {
  groups.forEach((group, idx) => {
    const path = options.pathPrefix ? `${options.pathPrefix}.composable_nodes_container[${idx}]` : `composable_nodes_container[${idx}]`;
    const block = renderComposableContainer(group, { ...options, path });

    container.appendChild(block);
    options.renderBlock(block, 'composable-container');
  });
}

export function renderComposableContainer(group, options = {}) {
  const composableContainer = renderBaseBlock({
    type: 'composable-container',
    options: {
      ...options,
      events: group.events
    }
  });

  // Header
  const header = document.createElement('div');
  header.className = 'composable-container-header';

  // Render additional sections
  const metaSections = [
    { key: 'target_container', icon: '📛', label: 'Container', value: group.target_container },
    { key: 'package', icon: '📦', label: 'Package', value: group.package },
    { key: 'executable', icon: '▶️', label: 'Executable', value: group.executable },
    { key: 'output', icon: '🖥️', label: 'Output', value: group.output }
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

  composableContainer.append(header);

  // Body
  const body = document.createElement('div');
  body.className = 'composable-container-body';
  composableContainer.appendChild(body);

  const innerLayoutManager = new LayoutManager(20, 40, 80, 40);
  const childOptions = {
    ...options,
    stopPropagation: true,
    constrainToParent: true,
    pathPrefix: `${options.path}`,
    renderBlock: (block, columnType) => {
      requestAnimationFrame(() => {
        innerLayoutManager.placeBlock(block, columnType);
      });
    }
  };

  // Render composable nodes
  renderComponent(
    { type: 'composable_nodes', value: group.composable_nodes, namespace: group.namespace },
    body, childOptions
  );

  renderAutoResizableBody(composableContainer, 'block', ['.composable-container-header']);

  return composableContainer;
}
