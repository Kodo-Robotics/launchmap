"""
Node Handler for ROS 2 Launch File AST Parser

This module extracts and parses the 'Node' action from a ROS 2 launch file,
handling common fields and launch-time configurations.

✅ Supported Node Fields (Static Parsing):
- package (str)
- executable (str)
- name (str, optional)
- namespace (str, optional)
- output (e.g., "screen", optional)
- parameters:
    - List of inline dictionaries
    - YAML file paths as strings
    - LaunchConfiguration with/without default
    - Direct dictionary (not in a list)
- remappings:
    - List of 2-element tuples

⚠️ Partially Supported / Fallback as "<unresolved>":
- Parameters set via variable reference
- LaunchConfiguration combined with other substitutions
- Fields assigned from variables
- Mixed types or nested launch expressions

🛑 Not Supported by Static Parsing:
- Node constructed conditionally (e.g., in if/else or loops)
- Node returned from factory/helper functions
- Parameters returned from functions (e.g., load_params())
- Any dynamic logic requiring runtime evaluation

For unsupported or ambiguous cases, the handler inserts a fallback value
(e.g., "<unresolved>" or symbolic LaunchConfiguration placeholder)
to keep output consistent and informative.

"""

import ast
from parser.context import ParseContext
from parser.utils import get_kwarg, parse_value, parse_dict

def handle_node(node: ast.Call, ctx: ParseContext) -> dict:
    if not isinstance(node, ast.Call):
        return None
    
    fields = ["package", "executable", "name", "namespace", "output"]
    data = {}

    for field in fields:
        value = get_kwarg(node, field)
        if value:
            field_ctx = ParseContext(visitor=ctx.visitor, field=field)
            data[field] = parse_value(value, field_ctx)
    
    # Parameters
    params = get_kwarg(node, "parameters")
    param_ctx = ParseContext(visitor=ctx.visitor, field="parameters")
    parsed_params = []

    if isinstance(params, ast.List):
        for elt in params.elts:
            parsed = parse_value(elt, param_ctx)
            parsed_params.append(parsed)

    elif isinstance(params, ast.Dict):
        parsed = parse_value(params, param_ctx)
        parsed_params.append(parsed)

    elif params is not None:
        parsed = parse_value(params, param_ctx)
        if isinstance(parsed, list):
            parsed_params.extend(parsed)
        else:
            parsed_params.append(parsed)
    
    if parsed_params:
        data["parameters"] = parsed_params

    # Remappings
    remaps = get_kwarg(node, "remappings")
    if remaps and isinstance(remaps, ast.List):
        pairs = []
        for elt in remaps.elts:
            if isinstance(elt, ast.Tuple) and len(elt.elts) == 2:
                remap_ctx = ParseContext(visitor=ctx.visitor, field="remappings")
                lhs = parse_value(elt.elts[0], remap_ctx)
                rhs = parse_value(elt.elts[1], remap_ctx)
                pairs.append([lhs, rhs])
        data["remappings"] = pairs
    
    # Arguments
    arguments = get_kwarg(node, "arguments")
    if arguments and isinstance(arguments, ast.List):
        arg_ctx = ParseContext(visitor=ctx.visitor, field="arguments")
        data["arguments"] = [parse_value(arg, arg_ctx) for arg in arguments.elts]
    
    return data
