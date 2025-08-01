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
from parser.tests.test_helpers import load_yaml_tests, load_custom_handler_tests, parse_launch_string

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/node_tests.yaml"))
def test_node_parsing(code, expected):
    result = parse_launch_string(code)
    assert result.get("nodes") == expected.get("nodes")

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/launch_config_tests.yaml"))
def test_launch_configuration_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["nodes", "arguments", "includes", "groups", "parameters", 
                "launch_argument_usages", "undeclared_launch_configurations"]:
        assert result.get(key, []) == expected.get(key, [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/group_action_tests.yaml"))
def test_group_action_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["nodes", "arguments", "includes", "groups", "launch_argument_usages"]:
        assert result.get(key, []) == expected.get(key, [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/include_launch_tests.yaml"))
def test_include_launch_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["arguments", "includes", "launch_argument_usages", "undeclared_launch_configurations"]:
        assert result.get(key, []) == expected.get(key, [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/opaque_function_tests.yaml"))
def test_opaque_functions_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["arguments", "opaque_functions", "launch_argument_usages", "undeclared_launch_configurations"]:
        assert result.get(key, []) == expected.get(key, [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/condition_tests.yaml"))
def test_conditions_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["arguments", "nodes", "groups", "launch_argument_usages", "undeclared_launch_configurations"]:
        assert result.get(key, []) == expected.get(key, [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/composable_node_tests.yaml"))
def test_composable_nodes_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["arguments", "composable_nodes", "unattached_composable_nodes", "launch_argument_usages", "undeclared_launch_configurations"]:
        assert result.get(key, []) == expected.get(key, [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/event_handler_tests.yaml"))
def test_event_handlers_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["nodes", "event_handlers"]:
        assert result.get(key, []) == expected.get(key, [])

@pytest.mark.parametrize("code,expected", load_custom_handler_tests("test_cases/custom_handlers_tests.yaml", "test_handlers"))
def test_custom_handlers_parsing(code, expected):
    result = parse_launch_string(code)
    for key in ["arguments", "nodes", "launch_argument_usages", "custom_components"]:
        assert result.get(key, []) == expected.get(key, [])

# @pytest.mark.parametrize("code,expected,files", load_yaml_tests("test_cases/recursive_include_tests.yaml", with_files=True))
# def test_recursive_include_parsing(code, expected, files):
#     with mock_tempfile_and_fs(code, files):
#         result = parse_launch_string(code)

#     for key in ["nodes", "arguments", "includes", "groups", "launch_argument_usages"]:
#         assert result.get(key, []) == expected.get(key, [])