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

import tempfile

import pytest
import yaml

from parser.entrypoint.user_interface import parse_and_format_launch_file
from parser.plugin_loader import load_user_handlers_from_directory


def load_yaml_tests(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    tests = []
    for test in data["tests"]:
        code = test["input"]
        expected = test["expected"]
        test_id = test.get("name", "Unnamed Test")
        tests.append(pytest.param(code, expected, id=test_id))

    return tests


def load_custom_handler_tests(file_path, handler_directory):
    load_user_handlers_from_directory(handler_directory)
    return load_yaml_tests(file_path)


def parse_launch_string(code: str, suffix) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False) as tmp:
        tmp.write(code)
        tmp.flush()
        return parse_and_format_launch_file(tmp.name)
