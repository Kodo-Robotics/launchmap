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

import { makeDraggable } from '../drag.js';
import { renderNodeGroup } from './renderNode.js';
import { renderIncludesGroup } from './renderInclude.js';
import { renderSection } from './renderSection.js';

export function renderGroupGroup(container, groups, namespace, layoutCtx, options = {}) {
    groups.forEach((group, idx) => {
        const path = options.pathPrefix ? `${options.pathPrefix}[${idx}]` : `groups[${idx}]`;
        renderGroup(group, path, container, layoutCtx, { ...options, path });
    });

    layoutCtx.x += 350;
    layoutCtx.y = 100;
}

export function renderGroup(group, prefix, container, layoutCtx, options = {}) {
    const ns = group.namespace || prefix;
    const groupBox = document.createElement("div");
    groupBox.className = "group-box";
    groupBox.style.left = `${layoutCtx.x}px`;
    groupBox.style.top = `${layoutCtx.y}px`;
    groupBox.style.position = "absolute";

    // Header
    const header = document.createElement("div");
    header.className = "group-header";

    // Title
    const title = document.createElement("div");
    title.className = "group-title";
    title.innerText = `📦 Group: ${ns}`;
    header.appendChild(title);

    // Namespace
    if (group.namespace) {
        const nsSection = renderSection("namespace", "🧭", "Namespace", group.namespace, 
            { includeLeftPort: true, portIdPrefix: options.path, portRegistry: options.portRegistry });
        nsSection.classList.add("namespace-section");
        header.appendChild(nsSection);
    }
    groupBox.appendChild(header);

    groupBox.dataset.path = prefix;
    groupBox.dataset.type = "group";
    if (options.blockRegistry) {
        options.blockRegistry[prefix] = groupBox;
    }

    // Body
    const body = document.createElement("div");
    body.className = "group-body";
    groupBox.appendChild(body);

    const innerLayout = { x: 20, y: 40 };
    const childOptions = { 
        ...options,
        stopPropagation: true, 
        constrainToParent: true,
        pathPrefix: `${prefix}.nodes`
    };

    const actions = group.actions;

    renderNodeGroup(body, actions.nodes || [], ns, innerLayout, childOptions);
    renderIncludesGroup(body, actions.includes || [], ns, innerLayout, {
        ...childOptions,
        pathPrefix: `${prefix}.includes`
    });
    (actions.groups || []).forEach((subgroup, idx) => {
        const subPrefix = `${prefix}.groups[${idx}]`;
        renderGroup(subgroup, subPrefix, body, innerLayout, {
            ...childOptions,
            path: subPrefix
        });
    });

    container.appendChild(groupBox);
    makeDraggable(groupBox, {
        ...options,
        onDrag: () => {
            if (options.renderEdges && options.parsedData && options.argumentRegistry && options.blockRegistry) {
                options.renderEdges(options.parsedData, options.portRegistry);
            }
        }
    });

    requestAnimationFrame(() => {
        const children = groupBox.querySelectorAll(".node-block, .include-block");
        let maxRight = 0;
        let maxBottom = 0;

        children.forEach(child => {
            const rect = child.getBoundingClientRect();
            const parentRect = groupBox.getBoundingClientRect();
            const right = rect.right - parentRect.left;
            const bottom = rect.bottom - parentRect.top;

            if (right > maxRight) maxRight = right;
            if (bottom > maxBottom) maxBottom = bottom;
        });

        groupBox.style.width = `${maxRight + 20}px`;
        groupBox.style.height = `${maxBottom + 20}px`;
    });

    layoutCtx.x += 350;
}