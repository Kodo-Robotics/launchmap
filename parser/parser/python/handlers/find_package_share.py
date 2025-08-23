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


@register_handler("FindPackageShare", "launch.substitutions.FindPackageShare")
def handle_find_package_share(node: ast.Call, context: ParseContext) -> dict:
    args, _ = resolve_call_signature(node, context.engine)
    if not args:
        raise ValueError("FindPackageShare requires a package name.")

    return {"type": "FindPackageShare", "package": args[0]}
