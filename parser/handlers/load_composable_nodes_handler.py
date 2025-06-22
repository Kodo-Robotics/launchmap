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
from parser.utils import get_kwarg, parse_value, resolve_starred_list
from parser.handlers.composable_node_handler import handle_composable_node

def handle_load_composable_nodes(node: ast.Call, ctx: ParseContext) -> dict:
    if not isinstance(node, ast.Call) or getattr(node.func, "id", None) != "LoadComposableNodes":
        return None
    
    data = {}
    container = get_kwarg(node, "target_container")
    if container:
        container_ctx = ParseContext(ctx.visitor, field="target_container")
        data["target_container"] = parse_value(container, container_ctx)

    composable_nodes = []
    children = []

    # Resolve list of composable nodes
    if node.args and isinstance(node.args[0], ast.List):
        children = resolve_starred_list(node.args[0].elts, ctx.visitor)
    else:
        comp_descs_kwarg = get_kwarg(node, "composable_node_descriptions")
        if isinstance(comp_descs_kwarg, ast.List):
            children = resolve_starred_list(comp_descs_kwarg.elts, ctx.visitor)
        elif isinstance(comp_descs_kwarg, ast.Name) and comp_descs_kwarg.id in ctx.visitor.assignments:
            resolved = ctx.visitor.assignments[comp_descs_kwarg.id]
            if isinstance(resolved, ast.List):
                children = resolve_starred_list(resolved.elts, ctx.visitor)

    for idx, child in enumerate(children):
        actual_node = child
        if isinstance(child, ast.Name) and child.id in ctx.visitor.assignments:
            actual_node = ctx.visitor.assignments[child.id]
        
        if isinstance(actual_node, ast.Call) and getattr(actual_node.func, "id", None) == "ComposableNode":
            path_label = f"composable_nodes[{idx}]"
            node_data = ctx.visitor.with_path(path_label, handle_composable_node, actual_node)
            if node_data:
                composable_nodes.append(node_data)
    
    if composable_nodes:
        data["composable_nodes"] = composable_nodes

    return data if data else None