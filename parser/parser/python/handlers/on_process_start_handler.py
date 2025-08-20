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


@register_handler("OnProcessStart", "launch_ros.handlers.OnProcessStart")
def handle_on_process_start(node: ast.Call, context: ParseContext):
    args, kwargs = resolve_call_signature(node, context.engine)

    target_actions = kwargs.get("target_action")
    triggered_actions = kwargs.get("on_start")

    if not isinstance(target_actions, list):
        target_actions = [target_actions]
    if not isinstance(triggered_actions, list):
        triggered_actions = [triggered_actions]

    # Assign symbolic reference
    handler_idx = context.introspection.next_event_handler_index()
    handler_ref = f"${{EventHandler[{handler_idx}]:OnProcessStart}}"

    # Update target action
    for target in target_actions:
        target.setdefault("events", {}).setdefault("triggers", []).append(handler_ref)
        context.introspection.register_entity(target)

    for triggered in triggered_actions:
        triggered.setdefault("events", {}).setdefault("triggered_by", []).append(handler_ref)
        context.introspection.register_entity(triggered)

    # Register event handler metadata
    context.introspection.add_event_handler("OnProcessStart")

    return {"type": "OnProcessStart"}
