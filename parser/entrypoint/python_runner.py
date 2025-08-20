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
from parser.entrypoint.common import build_result
from parser.parser.python.utils import collect_function_defs
from parser.resolution.resolution_engine import ResolutionEngine


def parse_python_launch_file(filepath: str) -> dict:
    """
    Entrypoint: parses a launch file and returns structured output
    Detects LaunchDescription([...]) or ld.add_action(...) usage.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code, filename=filepath)

    # Set up shared context and resolution engine
    context = ParseContext()
    context.current_file = filepath
    engine = ResolutionEngine(context)
    context.engine = engine

    parsed = []

    collect_function_defs(tree.body, context)

    # Simulate top-level execution
    for node in tree.body:
        if isinstance(node, ast.Assign):
            engine.resolve(node)

        elif isinstance(node, ast.Expr):
            engine.resolve(node)

    # Now extract and run generate_launch_description
    main_fn = context.lookup_function("generate_launch_description")
    if not main_fn:
        raise ValueError("No generate_launch_description() function found.")

    parsed.extend(_parse_launch_function_body(main_fn.body, context, engine))

    return build_result(filepath, context, parsed)


def _parse_launch_function_body(
    body: list[ast.stmt], context: ParseContext, engine: ResolutionEngine
) -> list:
    parsed = []
    for stmt in body:
        if isinstance(stmt, ast.Assign):
            engine.resolve(stmt)

        elif isinstance(stmt, ast.If):
            engine.resolve(stmt)

        elif isinstance(stmt, ast.Expr):
            func_name = context.get_func_name(stmt.value.func)
            if func_name.endswith("add_action"):
                arg = stmt.value.args[0]
                result = engine.resolve(arg)
                if result:
                    parsed.append(result)
            else:
                engine.resolve(stmt)

        elif isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Call):
            resolved = engine.resolve(stmt.value)
            if isinstance(resolved, list):
                parsed.extend(resolved)
            elif resolved is not None:
                parsed.append(resolved)

    return parsed