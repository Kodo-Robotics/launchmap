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

import pytest

from parser.tests.test_helpers import (
    load_custom_handler_tests,
    load_yaml_tests,
    parse_launch_string,
)

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/node_xml_tests.yaml"))
def test_node_parsing(code, expected):
    result = parse_launch_string(code, suffix=".xml")
    print(result)
    print(expected)
    assert result.get("nodes") == expected.get("nodes")
