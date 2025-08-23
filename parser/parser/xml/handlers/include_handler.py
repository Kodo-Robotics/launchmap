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

from xml.etree import ElementTree as ET

from parser.context import ParseContext
from parser.parser.registry import register_handler
from parser.parser.xml.handlers.condition_handler import handle_condition
from parser.parser.xml.utils import resolve_children, resolve_parameters


@register_handler("include")
def handle_include(element: ET.Element, context: ParseContext) -> dict:
    """
    Handle an XML <include> tag.
    Processes attributes and child tags (arg).
    """
    kwargs = {}
    kwargs.update(resolve_parameters(element, context))
    handle_condition(kwargs)

    launch_source = kwargs.get("file")
    condition = kwargs.get("condition", None)

    # Extract launch arguments
    launch_args = {}
    children = resolve_children(element, context)
    for child in children:
        if child["type"] == "LaunchArguments":
            launch_args.update(child["value"])

    result = {
        "type": "IncludeLaunchDescription",
        "launch_description_source": launch_source,
        "launch_arguments": launch_args,
        "included": {},
    }

    if condition:
        result["condition"] = condition

    return result
