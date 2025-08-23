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
from parser.parser.xml.utils import resolve_parameters


@register_handler("env")
def handle_environment_variable(element: ET.Element, context: ParseContext):
    """
    Handle <env> tag.
    Converts XML attributes (name, value) into a key-value dictionary entry.
    """
    kwargs = {}
    kwargs.update(resolve_parameters(element, context))

    name, value = kwargs["name"], kwargs["value"]

    # Track environment variable usage
    context.introspection.track_environment_variable(kwargs["name"], kwargs)

    return {"type": "EnvironmentVariable", "name": name, "value": value}


@register_handler("subst:env")
def handle_environment_variable_substitution(name: str, context: ParseContext) -> dict:
    """
    Handle $(eval) substitution
    """
    return {"type": "EnvironmentVariable", "name": name}
