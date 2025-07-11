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
from parser.parser.utils.common import flatten_once, group_entities_by_type
from parser.resolution.utils import resolve_call_signature

@register_handler("LoadComposableNodes", "launch_ros.actions.LoadComposableNodes")
def handle_load_composable_nodes(node: ast.Call, context: ParseContext) -> dict:
    args, kwargs = resolve_call_signature(node, context.engine)

    # Resolve composable nodes
    raw_nodes = kwargs.get("composable_node_descriptions" or (args[0] if args else []))
    resolved_flat = flatten_once(raw_nodes)
    grouped = group_entities_by_type(resolved_flat)
    composable_nodes = grouped.get("unattached_composable_nodes", [])

    # Determine target container
    target_container = kwargs.get("target_container")
    if not target_container:
        raise ValueError("LoadComposableNodes requires a target_container to be specified.")

    # Ensure group is registered
    context.register_composable_node_group(target_container, {"target_container": target_container})
    context.extend_composable_node_group(target_container, composable_nodes)

    return {
        "type": "LoadComposableNodes",
        "target_container": target_container   
    }