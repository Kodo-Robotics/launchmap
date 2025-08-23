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
from parser.parser.xml.utils import normalize_keys, resolve_children, resolve_parameters


@register_handler("node")
def handle_node(element: ET.Element, context: ParseContext) -> dict:
    """
    Handle an XML <node> tag.
    Processes attributes and child tags (param, remap and env).
    """
    kwargs = {}
    kwargs.update(resolve_parameters(element, context))
    handle_condition(kwargs)

    # Resolve remapping and parameters
    remappings = []
    parameters = {}
    environment_vars = {}
    children = resolve_children(element, context)
    for child in children:
        if child["type"] == "Remapping":
            remappings.append(child["value"])
        elif child["type"] == "SetParameter":
            parameters.update({child["name"]: child["value"]})
        elif child["type"] == "EnvironmentVariable":
            environment_vars.update({child["name"]: child["value"]})

    if len(remappings) > 0:
        kwargs["remappings"] = remappings
    if len(parameters) > 0:
        kwargs["parameters"] = parameters
    if len(environment_vars) > 0:
        kwargs["env"] = environment_vars

    # Resolve namespace
    if "namespace" not in kwargs:
        ns = context.current_namespace()
        if ns:
            kwargs["namespace"] = ns

    norm_kwargs = normalize_keys(
        kwargs, {"pkg": "package", "exec": "executable"}
    )
    return {"type": "Node", **norm_kwargs}
