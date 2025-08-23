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
from parser.parser.xml.utils import normalize_keys, resolve_parameters


@register_handler("arg")
def handle_arg(element: ET.Element, context: ParseContext) -> dict:
    """
    Handle an XML <arg> tag.
    - Tracks the declared argument in introspection
    """
    kwargs = {}
    kwargs.update(resolve_parameters(element, context))

    # Detect if arg is used inside include tag
    arg_value = kwargs.get("value", None)
    if arg_value:
        return {"type": "LaunchArguments", "value": {kwargs["name"]: kwargs["value"]}}

    # Track for introspection
    arg_name = kwargs.get("name")
    if arg_name:
        context.introspection.track_launch_arg_declaration(arg_name, kwargs)

    norm_kwargs = normalize_keys(kwargs, {"default": "default_value"})
    return {"type": "DeclareLaunchArgument", **norm_kwargs}
