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
from parser.parser.python.registry import register_handler
from parser.parser.utils.ast_utils import extract_opaque_function
from parser.parser.utils.common import group_entities_by_type
from parser.resolution.resolution_engine import ResolutionEngine
from parser.resolution.utils import bind_function_args, resolve_call_signature


@register_handler("OpaqueFunction", "launch.actions.OpaqueFunction")
def handle_opaque_function(node: ast.Call, context: ParseContext) -> dict:
    args, kwargs = resolve_call_signature(node, context.engine)

    fn_candidate = kwargs.get("function") or (args[0] if args else None)

    if isinstance(fn_candidate, ast.FunctionDef):
        function_name = fn_candidate.name
        fn_def = fn_candidate
    elif isinstance(fn_candidate, str):
        function_name = fn_candidate
        fn_def = context.lookup_function(function_name)
        if not fn_def:
            raise ValueError(f"Function '{function_name}' not found in parsed context.")
    else:
        raise ValueError("OpaqueFunction 'function' must be a string or FunctionDef.")

    # Get full function signature
    param_parts = [arg.arg for arg in fn_def.args.args]
    if fn_def.args.vararg:
        param_parts.append(f"*{fn_def.args.vararg.arg}")
    if fn_def.args.kwarg:
        param_parts.append(f"**{fn_def.args.kwarg.arg}")
    full_signature = f"{fn_def.name}({', '.join(param_parts)})"

    # Build symbolic context
    symbolic_context = ParseContext(context.introspection)
    symbolic_context.strategy = "symbolic"

    # Bind arguments and inject into symbolic context
    user_args = simplify_launch_configurations(
        kwargs.get("args", []) if isinstance(kwargs.get("args"), list) else []
    )
    user_kwargs = simplify_launch_configurations(
        kwargs.get("kwargs", []) if isinstance(kwargs.get("kwargs"), dict) else {}
    )
    param_binding = bind_function_args(fn_def, user_args, user_kwargs, True)
    for var_name, value in param_binding.items():
        symbolic_context.define_variable(var_name, value)

    # Build symbolic engine
    symbolic_engine = ResolutionEngine(symbolic_context)
    symbolic_context.engine = symbolic_engine

    # Extract returned data and symbolic usage from function body
    result = extract_opaque_function(fn_def, context, symbolic_engine)
    grouped = group_entities_by_type(result)

    return {"type": "OpaqueFunction", "name": full_signature, "returns": grouped}
