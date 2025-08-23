# Copyright (c) 2025 Kodo Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast

from parser.context import ParseContext
from parser.parser.registry import register_handler
from parser.parser.utils import flatten_once, group_entities_by_type
from parser.resolution.utils import resolve_call_signature


@register_handler("ComposableNodeContainer", "launch_ros.actions.ComposableNodeContainer")
def handle_composable_container(node: ast.Call, context: ParseContext) -> dict:
    args, kwargs = resolve_call_signature(node, context.engine)

    # Resolve composable nodes
    raw_expr = kwargs.get("composable_node_descriptions") or (args[0] if args else [])
    resolved_flat = flatten_once(raw_expr)
    grouped = group_entities_by_type(resolved_flat)
    composable_nodes = grouped.get("unattached_composable_nodes", [])

    # Extract container name to associate with target_container
    container_name = kwargs.get("name") or "anonymous_container"

    # Collect container metadata
    container_metadata = {
        "target_container": container_name,
    }
    for key, value in kwargs.items():
        if key not in {"composable_node_descriptions", "name"}:
            container_metadata[key] = value

    # Register container and attach nodes
    context.register_composable_node_group(container_name, container_metadata)
    context.extend_composable_node_group(container_name, composable_nodes)

    return {"type": "ComposableNodeContainer", "target_container": container_name}
