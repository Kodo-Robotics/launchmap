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
from xml.etree import ElementTree as ET

from parser.context import ParseContext
from parser.parser.loader import register_builtin_handlers
from parser.parser.registry import get_handler
from parser.resolution.utils import get_func_name

register_builtin_handlers()


def dispatch_call(node: ast.Call, context: ParseContext) -> dict:
    """
    Dispatch a launch construct call to its registered handler.

    - Extracts full dotted name of the function (launch_ros.actions.Node)
    - Looks up in handler registry
    - Delegates handling to the registered handler
    """
    func_name = get_func_name(node.func)
    handler = get_handler(func_name)

    if not handler:
        raise ValueError(f"Unrecognized launch construct: '{func_name}'")

    return handler(node, context)

def dispatch_element(el: ET.Element, context: ParseContext) -> dict:
    """
    Dispatch a launch construct (XML element) to its registered handler.

    - Uses the raw tag name ('node', 'include', 'group')
    - Looks up the handler in registry
    - Delegates to handler
    """
    tag = _strip_ns(el.tag)
    handler = get_handler(tag)

    if not handler:
        raise ValueError(f"Unrecognized XML launch construct: <{tag}>")

    return handler(el, context)

def _strip_ns(tag: str) -> str:
    return tag.split('}')[-1]
