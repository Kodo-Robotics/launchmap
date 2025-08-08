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
from parser.resolution.loader import register_builtin_resolvers
from parser.resolution.utils import try_all_resolvers


class ResolutionEngine:
    def __init__(self, context: ParseContext):
        register_builtin_resolvers()
        self.context = context
        self.context.engine = self

    def resolve(self, node: ast.AST):
        return try_all_resolvers(node, self)
