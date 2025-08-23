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

import os
import sys
import json
import argparse
from parser.entrypoint.user_interface import parse_and_format_launch_file
from parser.plugin_loader import load_user_handlers_from_directory

DEFAULT_PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "parser", "custom_handler")

def main():
    parser = argparse.ArgumentParser(description="Parse a ROS2 launch file.")
    parser.add_argument("launch_file", help="Path to launch file to parse.")
    parser.add_argument(
        "--plugin-dir", help="Directory containing user-defined custom handlers.",
        default = DEFAULT_PLUGIN_DIR
    )

    args = parser.parse_args()

    if os.path.isdir(args.plugin_dir):
        load_user_handlers_from_directory(args.plugin_dir)

    try:
        result = parse_and_format_launch_file(args.launch_file)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
