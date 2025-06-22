import { renderComposableNodeGroup } from './renderComposableNode.js';
import { makeDraggable } from '../drag.js'
import { renderSection } from './renderSection.js';

export function renderComposableGroup(group, prefix, container, layoutCtx, options = {}) {
    const ns = group.namespace || prefix;
    const box = document.createElement("div");
    box.className = "group-box";
    box.style.left = `${layoutCtx.x}px`;
    box.style.top = `${layoutCtx.y}px`;
    box.style.position = "absolute";

    // Header
    const header = document.createElement("div");
    header.className = "group-header";

    // Title
    const title = document.createElement("div");
    title.className = "group-title";
    title.innerText = `🧩 Composable Group: ${ns}`;
    header.appendChild(title);

    // Target container
    if (group.target_container) {
        const target = renderSection(
            "target_container",
            "📦",
            "Target Container",
            `<code>${group.target_container}</code>`,
            {
                includeLeftPort: true,
                portIdPrefix: prefix,
                portRegistry: options.portRegistry,
            }
        );
        header.appendChild(target);
    }
    
    box.appendChild(header);
    container.appendChild(box);

    if (options.blockRegistry) {
        box.dataset.path = prefix;
        box.dataset.type = "composable_group";
        options.blockRegistry[prefix] = box;
    }

    // Body
    const body = document.createElement("div");
    body.className = "group-body";
    box.appendChild(body);

    const innerLayout = { x: 20, y: 40 };
    const childOptions = { 
        ...options,
        stopPropagation: true, 
        constrainToParent: true,
        pathPrefix: `${prefix}.composable_nodes`
    };
    renderComposableNodeGroup(body, group.composable_nodes || [], "", innerLayout, childOptions);

    makeDraggable(box, {
        ...options,
        onDrag: () => {
            if (options.renderEdges && options.parsedData && options.argumentRegistry && options.blockRegistry) {
                options.renderEdges(options.parsedData, options.portRegistry);
            }
        }
    });

    requestAnimationFrame(() => {
        const children = box.querySelectorAll(".node-block");
        let maxRight = 0;
        let maxBottom = 0;

        children.forEach(child => {
            const rect = child.getBoundingClientRect();
            const parentRect = box.getBoundingClientRect();
            const right = rect.right - parentRect.left;
            const bottom = rect.bottom - parentRect.top;

            if (right > maxRight) maxRight = right;
            if (bottom > maxBottom) maxBottom = bottom;
        });

        box.style.width = `${maxRight + 20}px`;
        box.style.height = `${maxBottom + 20}px`;
    });

    layoutCtx.x += 350;
}