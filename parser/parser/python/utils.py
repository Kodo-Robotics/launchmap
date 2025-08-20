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


def collect_function_defs(body: list[ast.stmt], context: ParseContext):
    """
    Recursively collect all FunctionDef nodes inside a body list
    and register them into the context.
    """
    for stmt in body:
        if isinstance(stmt, ast.FunctionDef):
            context.define_function(stmt.name, stmt)

        # Recursively handle compound statements
        for attr in ("body", "orelse", "finalbody"):
            inner = getattr(stmt, attr, None)
            if isinstance(inner, list):
                collect_function_defs(inner, context)


def extract_opaque_function(fn_def: ast.FunctionDef, context, symbolic_engine):
    """
    Execute the body of an OpaqueFunction symbolically and return parsed results.
    """
    body = fn_def.body
    result = None

    for stmt in body:
        if isinstance(stmt, ast.Assign):
            symbolic_engine.resolve(stmt)

        elif isinstance(stmt, ast.Expr):
            symbolic_engine.resolve(stmt)

        elif isinstance(stmt, ast.Return):
            if stmt.value is None:
                return None

            result = symbolic_engine.resolve(stmt.value)
            break

    return result
