import { makeDraggable } from "../drag.js";
import { renderSection } from "./renderSection.js";

export function renderComposableNodeGroup(container, nodes, namespace, layoutCtx, options = {}) {
    nodes.forEach((node, idx) => {
        const path = options.pathPrefix ? `${options.pathPrefix}[${idx}]` : "";
        const block = renderComposableNode(node, namespace, layoutCtx, { ...options, path });
        container.appendChild(block);
        layoutCtx.y += 100;
    });
    layoutCtx.x += 250;
    layoutCtx.y = 100;
}

function renderComposableNode(node, namespace, layoutCtx, options) {
    const block = document.createElement("div");
    block.className = "composable-node-block";
    block.style.left = `${layoutCtx.x}px`;
    block.style.top = `${layoutCtx.y}px`;
    block.style.position = "absolute";

    const title = document.createElement("div");
    title.className = "composable-node-title";
    title.innerText = `${namespace}/${node.name || node.plugin}`;
    block.appendChild(title);

    const renderOptions = {
        includeLeftPort: true,
        portIdPrefix: options.path,
        portRegistry: options.portRegistry
    };
    
    block.appendChild(renderSection("package", "📦", "Package", `<code>${node.package}</code>`, renderOptions));
    block.appendChild(renderSection("plugin", "🔌", "Plugin", `<code>${node.plugin}</code>`, renderOptions));

    if (node.parameters?.length > 0) {
        let paramHtml = "<ul>";
        for (const p of node.parameters) {
            if (typeof p === "object" && !Array.isArray(p)) {
                for (const [k, v] of Object.entries(p)) {
                    paramHtml += `<li><code>${k}</code>: <code>${escapeHtml(String(v))}</code></li>`;
                }
            } else {
                paramHtml += `<li><code>${escapeHtml(String(p))}</code></li>`;
            }
        }
        paramHtml += "</ul>";
        block.appendChild(renderSection("parameters", "⚙️", "Params", paramHtml, renderOptions));
    }

    if (node.remappings?.length > 0) {
        const remapHtml = "<ul>" + node.remappings.map(([from, to]) =>
            `<li><code>${from}</code> → <code>${to}</code></li>`).join("") + "</ul>";
        block.appendChild(renderSection("remappings", "🔁", "Remap", remapHtml, renderOptions));
    }

    if (options.path) {
        block.dataset.path = options.path;
        block.dataset.type = "composable_node";
        if (options.blockRegistry) {
            options.blockRegistry[options.path] = block;
        }
    }

    makeDraggable(block, {
        ...options,
        onDrag: () => {
            if (options.renderEdges && options.parsedData && options.argumentRegistry && options.blockRegistry) {
                options.renderEdges(options.parsedData, options.portRegistry);
            }
        }
    });

    return block;
}

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;")
               .replace(/</g, "&lt;")
               .replace(/>/g, "&gt;")
               .replace(/"/g, "&quot;");
}