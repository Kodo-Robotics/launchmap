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

import json
import os

import pytest

from parser.entrypoint.user_interface import parse_and_format_launch_file
from parser.plugin_loader import load_user_handlers_from_directory

BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "real_cases/launch_files")
OUTPUT_DIR = os.path.join(BASE_DIR, "real_cases/expected_outputs")
PLUGIN_DIR = os.path.join(BASE_DIR, "../custom_handlers")


@pytest.mark.parametrize("filename", [f for f in os.listdir(INPUT_DIR) 
                                      if f.endswith(".py") or f.endswith(".xml")])
def test_real_launch_file_snapshot(filename):
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, f"{filename}.json")

    assert os.path.exists(output_path), f"Misssing expected output: {output_path}"

    load_user_handlers_from_directory(PLUGIN_DIR)
    result = parse_and_format_launch_file(input_path)
    expected = json.load(open(output_path))

    assert result == expected, f"Mismatch in output for {filename}"
