import ast
from parser.context import ParseContext
from parser.handlers.node_handler import handle_node
from parser.handlers.declare_argument_handler import handle_declare_argument
from parser.handlers.include_handler import handle_include
from parser.handlers.group_handler import handle_group_action

class LaunchFileVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = {
            "nodes": [],
            "arguments": [],
            "includes": [],
            "groups": [],
            "launch_argument_usages": [],
            "undeclared_launch_configurations": []
        }

        self.declared_arguments = set()
        self.used_arguments = []

        self.launch_arguments = set()
        self.path_stack = []

        self.assignments = {}
    
    def visit_Call(self, node: ast.Call):
        # Detect LaunchDescription([...])
        if isinstance(node.func, ast.Name) and node.func.id == "LaunchDescription":
            for arg in node.args:
                if isinstance(arg, ast.List):
                    for elt in arg.elts:
                        self._handle_action(elt)
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            self.assignments[var_name] = node.value
    
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Attribute) and call.func.attr == "add_action":
                arg = call.args[0]
                if isinstance(arg, ast.Name):
                    var_name = arg.id
                    action_node = self.assignments.get(var_name)
                    if action_node:
                        self._handle_action(action_node)
    
    def visit(self, node):
        super().visit(node)

        undeclared = []
        for usage in self.used_arguments:
            if usage not in self.declared_arguments:
                undeclared.append(usage)
        
        if undeclared:
            self.result["undeclared_launch_configurations"] = undeclared

    def track_launch_arg_usage(self, arg_name, field):
        usage = {
            "argument": arg_name,
            "field": field,
            "path": ".".join(self.path_stack) if self.path_stack else []
        }
        self.result.setdefault("launch_argument_usages", []).append(usage)

    def with_path(self, label: str, handler_fn, node) -> dict:
        self.path_stack.append(label)
        ctx = ParseContext(visitor = self)
        result = handler_fn(node, ctx)
        self.path_stack.pop()
        return result

    def _handle_action(self, node: ast.Call, into=None):
        target = into if into is not None else self.result
        func_id = getattr(node.func, 'id', None)

        def next_index(key):
            return len(target.get(key, []))

        if func_id == "Node":
            node_index = next_index("nodes")
            node_data = self.with_path(f"nodes[{node_index}]", handle_node, node)
            if node_data:
                target.setdefault("nodes", []).append(node_data)
        
        elif func_id == "DeclareLaunchArgument":
            arg_index = next_index("arguments")
            arg_data = self.with_path(f"arguments[{arg_index}]", handle_declare_argument, node)
            if arg_data:
                target.setdefault("arguments", []).append(arg_data)
        
        elif func_id == "IncludeLaunchDescription":
            include_index = next_index("includes")
            include_data = self.with_path(f"includes[{include_index}]", handle_include, node)
            if include_data:
                target.setdefault("includes", []).append(include_data)
        
        elif func_id == "GroupAction":
            group_index = next_index("groups")
            group_data = self.with_path(f"groups[{group_index}]", handle_group_action, node)
            if group_data:
                target.setdefault("groups", []).append(group_data)
        