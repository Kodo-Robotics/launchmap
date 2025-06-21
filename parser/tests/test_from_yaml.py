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

import yaml
import pytest
from parser.parser import parse_launch_string

def load_yaml_tests(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        return [
            pytest.param(test["input"], test["expected"], id=test["name"])
            for test in data["tests"]
        ]

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/node_tests.yaml"))
def test_node_parsing(code, expected):
    result = parse_launch_string(code)
    assert result.get("nodes") == expected.get("nodes")

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/node_params_edge.yaml"))
def test_node_params_edge_parsing(code, expected):
    result = parse_launch_string(code)
    assert result.get("nodes") == expected.get("nodes")

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/declare_argument_tests.yaml"))
def test_declare_argument_parsing(code, expected):
    result = parse_launch_string(code)
    assert result.get("arguments") == expected.get("arguments")

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/include_launch_tests.yaml"))
def test_include_launch_parsing(code, expected):
    result = parse_launch_string(code)
    assert result.get("includes") == expected.get("includes")

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/group_action_tests.yaml"))
def test_group_action_parsing(code, expected):
    result = parse_launch_string(code)
    assert result.get("groups") == expected.get("groups")

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/launch_argument_usage_tests.yaml"))
def test_launch_argument_usage_tracking(code, expected):
    result = parse_launch_string(code)
    assert result.get("arguments", []) == expected.get("arguments", [])
    assert result.get("groups", []) == expected.get("groups", [])
    assert result.get("includes", []) == expected.get("includes", [])
    print(result.get("launch_argument_usages", []))
    print(expected.get("launch_argument_usages", []))
    assert result.get("launch_argument_usages", []) == expected.get("launch_argument_usages", [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/variable_assignment_tests.yaml"))
def test_variable_assignment(code, expected):
    result = parse_launch_string(code)
    assert result.get("nodes", []) == expected.get("nodes", [])
    assert result.get("arguments", []) == expected.get("arguments", [])
    assert result.get("groups", []) == expected.get("groups", [])
    assert result.get("includes", []) == expected.get("includes", [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/undeclared_arguments_tests.yaml"))
def test_undeclared_arguments(code, expected):
    result = parse_launch_string(code)
    assert result.get("arguments", []) == expected.get("arguments", [])
    assert result.get("nodes", []) == expected.get("nodes", [])
    assert result.get("launch_argument_usages", []) == expected.get("launch_argument_usages", [])
    assert result.get("undeclared_launch_configurations", []) == expected.get("undeclared_launch_configurations", [])

@pytest.mark.parametrize("code,expected", load_yaml_tests("test_cases/composable_node_tests.yaml"))
def test_composable_node_parsing(code, expected):
    result = parse_launch_string(code)
    print(result.get("composable_nodes"))
    print(expected.get("composable_nodes"))
    assert result.get("composable_nodes") == expected.get("composable_nodes")