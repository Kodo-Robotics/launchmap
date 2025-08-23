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

import warnings
from typing import Any, Callable, Dict, Optional

from parser.context import ParseContext

# Handler signature: accepts a construct (AST Call, XML Element etc.) + context
Handler = Callable[[Any, "ParseContext"], Optional[dict]]

# Registry dictionary for known launch constructs
_HANDLER_REGISTRY: Dict[str, Handler] = {}


def register_handler(*names: str):
    """
    Decorator to register a handler for a given launch construct.
    
    For Python-based launch:
        @register_handler("Node", "launch_ros.actions.Node")

    For XML-based launch:
        @register_handler("node)

    You can register multiple aliases pointing to the same handler.
    """

    def decorator(func: Handler):
        for name in names:
            if name in _HANDLER_REGISTRY:
                warnings.warn(f"Overwriting existing handler for '{name}'")
            _HANDLER_REGISTRY[name] = func
        return func

    return decorator


def get_handler(name: str) -> Optional[Handler]:
    """
    Retrieve the handler for a given construct, or None if unregistered
    """
    return _HANDLER_REGISTRY.get(name)


def all_registered() -> Dict[str, Handler]:
    """
    Return the complete handler map (useful for debugging or listing).
    """
    return _HANDLER_REGISTRY.copy()
