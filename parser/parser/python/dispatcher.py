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
from parser.parser.python.loader import register_builtin_handlers
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
