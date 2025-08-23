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

from parser.entrypoint.user_interface import parse_and_format_launch_file
from parser.plugin_loader import load_user_handlers_from_directory

INPUT_DIR = "parser/tests/real_cases/launch_files"
OUTPUT_DIR = "parser/tests/real_cases/expected_outputs"
PLUGIN_DIR = "parser/tests/real_cases/launch_files/custom_handlers"

load_user_handlers_from_directory(PLUGIN_DIR)

for fname in os.listdir(INPUT_DIR):
    if fname.endswith(".py") or fname.endswith('.xml'):
        input_path = os.path.join(INPUT_DIR, fname)
        result = parse_and_format_launch_file(input_path)

        output_path = os.path.join(OUTPUT_DIR, f"{fname}.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"✅ Snapshot created: {output_path}")
