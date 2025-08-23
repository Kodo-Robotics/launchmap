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
from parser.resolution.utils import resolve_call_signature


@register_handler("DeclareLaunchArgument", "launch.actions.DeclareLaunchArgument")
def handle_declare_launch_argument(node: ast.Call, context: ParseContext) -> dict:
    """
    Handle DeclareLaunchArgument(name=..., default_value=..., description=...)
    - Tracks the declared argument in introspection
    """
    args, kwargs = resolve_call_signature(node, context.engine)

    # Positional fallback: first arg = name
    if "name" not in kwargs and args:
        kwargs["name"] = args[0]

    # Track for introspection
    arg_name = kwargs.get("name")
    if arg_name:
        context.introspection.track_launch_arg_declaration(arg_name, kwargs)

    return {"type": "DeclareLaunchArgument", **kwargs}
