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


@register_handler("PythonExpression", "launch.substitutions.PythonExpression")
def handle_if_condition(node: ast.Call, context: ParseContext) -> str:
    args, _ = resolve_call_signature(node, context.engine)

    if not args:
        raise ValueError("Python Expression requires at least one argument.")

    # Flatten and stringify all parts
    args = simplify_launch_configurations(args)
    if isinstance(args[0], list):
        expression = "".join(str(part) for part in args[0])
    else:
        expression = str(args[0])

    return expression
