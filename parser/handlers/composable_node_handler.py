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
from parser.utils import get_kwarg, parse_value
from parser.context import ParseContext

def handle_composable_node(node: ast.Call, ctx: ParseContext) -> dict:
    if not isinstance(node, ast.Call) or getattr(node.func, "id", None) != "ComposableNode":
        return None
    
    data = {}
    fields = ["package", "plugin", "name", "parameters"]

    for field in fields:
        value = get_kwarg(node, field)
        if value:
            field_ctx = ParseContext(visitor = ctx.visitor, field = field)
            parsed = parse_value(value, field_ctx)
            if parsed is not None:
                data[field] = parsed

    # Remappings
    remaps = get_kwarg(node, "remappings")
    if remaps and isinstance(remaps, ast.List):
        pairs = []
        for elt in remaps.elts:
            if isinstance(elt, ast.Tuple) and len(elt.elts) == 2:
                remap_ctx = ParseContext(visitor=ctx.visitor, field="remappings")
                lhs = parse_value(elt.elts[0], remap_ctx)
                rhs = parse_value(elt.elts[1], remap_ctx)
                pairs.append([lhs, rhs])
        data["remappings"] = pairs
    
    return data if data else None