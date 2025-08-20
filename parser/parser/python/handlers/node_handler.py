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
from parser.resolution.utils import resolve_call_kwargs


@register_handler("Node", "launch_ros.actions.Node")
def handle_node(node: ast.Call, context: ParseContext) -> dict:
    """
    Handle a launch_ros Node(...)
    Adds namespace context if not explicitly passed.
    """
    kwargs = resolve_call_kwargs(node, context.engine)

    if "namespace" not in kwargs:
        ns = context.current_namespace()
        if ns:
            kwargs["namespace"] = ns

    return {"type": "Node", **kwargs}
