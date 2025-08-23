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

import inspect

from parser.parser.registry import register_handler


def register_user_handler(type_name: str):
    """
    Decorator to register a user defined handler with validation.
    - Signature validation (must accept (node, context))
    - Output validation (must return dict with 'type': "CustomHandler", 'type_name': <type_name>)
    """

    def decorator(fn):
        # Check signature
        sig = inspect.signature(fn)
        expected_args = ["node", "context"]
        actual_args = list(sig.parameters.keys())

        if actual_args != expected_args:
            raise ValueError(
                f"User handler for '{type_name}' must have signature: "
                f"({', '.join(expected_args)}), but got: ({', '.join(actual_args)})"
            )

        # Wrap with validation
        def wrapper(node, context):
            result = fn(node, context)
            return result

        return register_handler(type_name)(wrapper)

    return decorator
