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

import importlib
import os
import pkgutil


def register_builtin_handlers():
    """
    Auto import all modules in parsers.handlers to trigger @register_handler decorators.
    """
    import parser.parser.handlers

    package_dir = os.path.dirname(parser.parser.handlers.__file__)
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):
        importlib.import_module(f"parser.parser.handlers.{module_name}")
