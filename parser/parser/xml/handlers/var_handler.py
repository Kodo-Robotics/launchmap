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

from xml.etree import ElementTree as ET

from parser.context import ParseContext
from parser.parser.registry import register_handler

@register_handler("var")
def handle_var(name: str, context: ParseContext) -> dict:
    """
    Handle $(var) substitution
    """
    context.introspection.track_launch_config_usage(name)
    return {"type": "LaunchConfiguration", "name": name}
