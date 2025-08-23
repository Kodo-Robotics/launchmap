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

from parser.parser.postprocessing import simplify_launch_configurations


def handle_condition(kwargs: dict):
    if "if" in kwargs:
        _handle_if_condition(kwargs)
    elif "unless" in kwargs:
        _handle_unless_condition(kwargs)

    return

def _handle_if_condition(kwargs: dict):
    expression = simplify_launch_configurations(kwargs["if"])
    kwargs.pop("if", None)
    kwargs["condition"] = f"${{IfCondition:{expression}}}"

def _handle_unless_condition(kwargs: dict):
    expression = simplify_launch_configurations(kwargs["unless"])
    kwargs.pop("unless", None)
    kwargs["condition"] = f"${{UnlessCondition:{expression}}}"