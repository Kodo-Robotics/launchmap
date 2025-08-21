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
from parser.parser.xml.utils import process_parameters


@register_handler("remap")
def handle_remap(element: ET.Element, context: ParseContext) -> dict:
    """
    Handle an <remap> tag.
    Converts <remap from="a" to="b" /> into ["a", "b"]
    """
    kwargs = {}
    kwargs.update(process_parameters(element, context))

    return {"remappings": [kwargs["from"], kwargs["to"]]}
