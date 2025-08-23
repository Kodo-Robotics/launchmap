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
from parser.parser.utils import flatten_once, group_entities_by_type
from parser.parser.xml.handlers.condition_handler import handle_condition
from parser.parser.xml.utils import resolve_parameters, resolve_children

@register_handler("group")
def handle_group(element: ET.Element, context: ParseContext) -> dict:
    """
    Handle an XML <group> tag.
    Processes attributes and child tags (param, remap and env).
    """
    kwargs = {}
    kwargs.update(resolve_parameters(element, context))
    handle_condition(kwargs)

    # Resolve 'actions' under group
    raw_expr = resolve_children(element, context)
    resolved_flat = flatten_once(raw_expr)

    namespace = None
    parameters = []
    actions = []
    for item in resolved_flat:
        if isinstance(item, dict) and item.get("type") == "PushROSNamespace":
            namespace = item.get("namespace")
            context.push_namespace(namespace)
        elif isinstance(item, dict) and item.get("type") == "SetParameter":
            parameters.append({item.get("name"): item.get("value")})
        else:
            actions.append(item)

    grouped = group_entities_by_type(actions)

    if namespace:
        context.pop_namespace()

    result = {
        "type": "GroupAction",
        **kwargs,
        "actions": grouped,
    }

    if namespace:
        result["namespace"] = namespace
    if parameters:
        result["parameters"] = parameters

    return result
