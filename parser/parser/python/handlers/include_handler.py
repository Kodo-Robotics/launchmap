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
from parser.parser.postprocessing import simplify_launch_configurations
from parser.parser.registry import register_handler
from parser.resolution.utils import resolve_call_signature


@register_handler("IncludeLaunchDescription", "launch.actions.IncludeLaunchDescription")
def handle_include(node: ast.Call, context: ParseContext) -> dict:
    """
    Handle IncludeLaunchDescription (launch_description_source=..., launch_arguments=...)
    - Resolves the included launch file via Include Resolver
    - Recursively parses the include file and merge results
    """
    args, kwargs = resolve_call_signature(node, context.engine)

    launch_source = kwargs.get("launch_description_source") or (args[0] if args else None)
    launch_args = kwargs.get("launch_arguments") or (args[1] if len(args) > 1 else {})
    condition = kwargs.get("condition", None)

    if not isinstance(launch_source, dict) or "filename" not in launch_source:
        raise ValueError("Could not resolve include path from launch_description_source")

    file_value = launch_source["filename"]

    # Flatten and stringify all parts
    file_value = simplify_launch_configurations(file_value)
    if isinstance(file_value, list):
        path = "".join(str(part) for part in file_value)
    else:
        path = str(file_value)

    # Load and parse included file
    # from parser.includes.resolver import resolve_included_launch_file
    # included_output = resolve_included_launch_file(
    #     filename = launch_source["filename"],
    #     parent_context = context,
    #     passed_arguments = launch_args
    # )

    result = {
        "type": "IncludeLaunchDescription",
        "launch_description_source": path,
        "launch_arguments": launch_args,
        "included": {},
    }

    if condition:
        result["condition"] = condition

    return result
