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

from parser.entrypoint.common import detect_format_from_content
from parser.entrypoint.python_runner import parse_python_launch_file
from parser.entrypoint.xml_runner import parse_xml_launch_file


def parse_launch_file(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    kind = detect_format_from_content(code)

    if kind == "xml":
        return parse_xml_launch_file(filepath)
    return parse_python_launch_file(filepath)
