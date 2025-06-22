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

export function renderEdges(data, portRegistry) {
    const svg = document.getElementById("edge-layer");
    svg.innerHTML = "";

    (data.launch_argument_usages || []).forEach(usage => {
        const fromPortId = `argument:${usage.argument}:argument`;
        const toPortId = `${usage.path}:${usage.field}`

        const fromPort = portRegistry[fromPortId];
        const toPort = portRegistry[toPortId];

        if (!fromPort || !toPort) return;

        fromPort.classList.add("used-port");
        toPort.classList.add("used-port");

        const from = getCenter(fromPort);
        const to = getCenter(toPort);

        drawEdge(svg, from, to, usage.field);
    });
}

function getCenter(el) {
    const zoomLayer = document.getElementById("zoom-layer");
    const zoomRect = zoomLayer.getBoundingClientRect();
    const rect = el.getBoundingClientRect();

    const zoom = window.zoomState?.scale || 1;

    return {
        x: (rect.left - zoomRect.left + rect.width / 2) / zoom ,
        y: (rect.top - zoomRect.top + rect.height / 2) / zoom
    };
}

function drawEdge(svg, from, to, field) {
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");

    const dx = Math.abs(to.x - from.x);
    const controlOffset = Math.min(100, dx / 2);

    const d = `M ${from.x},${from.y} C ${from.x + controlOffset},${from.y} ${to.x - controlOffset},${to.y} ${to.x},${to.y}`;

    path.setAttribute("d", d);
    path.setAttribute("class", "edge-line");
    path.setAttribute("stroke", getEdgeColor(field));

    svg.appendChild(path);
}

function getEdgeColor(field) {
    switch (field) {
        case "parameters": return "#6aff6a";
        case "launch_arguments": return "#ffa500";
        case "namespace": return "#66ccff";
        case "target_container": return "#26c6da"; 
        default: return "#ccc";
    }
}