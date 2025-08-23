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

from typing import List

from parser.context import ParseContext


def build_result(filepath: str, context: ParseContext, parsed: List):
    """
    Shape the final response uniformly.
    """
    return {
        "file": filepath,
        "parsed": parsed,
        "used_launch_config": sorted(context.introspection.used_launch_configs),
        "declared_arguments": sorted(context.introspection.declared_launch_args.keys()),
        "undeclared_launch_configurations": sorted(
            context.introspection.get_undeclared_launch_configs()
        ),
        "environment_variables": context.introspection.get_environment_variables(),
        "python_expressions": context.introspection.get_python_expressions(),
        "composable_containers": context.get_composable_node_groups(),
        "additional_components": context.introspection.get_registered_entities(),
    }

def detect_format_from_content(code: str) -> str:
    """
    Return 'xml' if it parses as XML with <launch> root; otherwise 'python'.
    """
    head = code.lstrip().lower()
    if head.startswith("<?xml") or head.startswith("<launch"):
        return "xml"
    return "python"
