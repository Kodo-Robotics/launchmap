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
from parser.parser.registry import register_handler
from parser.resolution.utils import resolve_call_signature


@register_handler("FindExecutable", "launch.substitutions.FindExecutable")
def handle_find_executable(node: ast.Call, context: ParseContext) -> dict:
    args, kwargs = resolve_call_signature(node, context.engine)

    name = kwargs.get("name") or (args[0] if args else None)
    if not name:
        raise ValueError("FindExecutable requires the name of the executable.")

    return {"type": "FindExecutable", "name": name}
