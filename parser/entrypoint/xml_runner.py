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
from parser.entrypoint.common import build_result
from parser.parser.dispatcher import dispatch_element
from parser.utils.xml_utils import strip_ns


def parse_xml_launch_file(filepath: str) -> dict:
    """
    Entrypoint: parses a launch file and returns structured output
    Detects <launch>
    """
    root = ET.parse(filepath).getroot()
    tag = strip_ns(root.tag)
    if tag != "launch":
        raise ValueError(f"Expected <launch> as root tag, found <{tag}")

    # Set up shared context
    context = ParseContext()
    context.current_file = filepath

    parsed = []
    for child in list(root):
        result = dispatch_element(child, context)
        parsed.append(result)

    return build_result(filepath, parsed)
