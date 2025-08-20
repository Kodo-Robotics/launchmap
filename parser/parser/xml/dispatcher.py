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
from parser.parser.registry import get_handler
from parser.parser.xml.loader import register_builtin_handlers
from parser.parser.xml.utils import strip_ns

# register_builtin_handlers()

def dispatch_element(el: ET.Element, context: ParseContext) -> dict:
    """
    Dispatch a launch construct (XML element) to its registered handler.

    - Uses the raw tag name ('node', 'include', 'group')
    - Looks up the handler in registry
    - Delegates to handler
    """
    tag = strip_ns(el.tag)
    handler = get_handler(tag)

    if not handler:
        raise ValueError(f"Unrecognized XML launch construct: <{tag}>")

    return handler(el, context)