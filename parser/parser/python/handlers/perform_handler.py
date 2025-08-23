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

from parser.parser.registry import register_handler


@register_handler("perform")
def handle_perform(node: ast.Call, context):
    """
    Handles LaunchConfiguration(...).perform(context) by forwarding
    to the base substitution without actually invoking `.perform`.
    """
    if not isinstance(node.func, ast.Attribute):
        raise ValueError("Expected method call for '.perform()'")

    base_call_node = node.func.value
    return context.engine.resolve(base_call_node)
