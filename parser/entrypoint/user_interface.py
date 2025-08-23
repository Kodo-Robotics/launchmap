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

from parser.entrypoint.parser_runner import parse_launch_file
from parser.parser.introspection_utils import (
    collect_composable_node_containers,
    collect_environment_variable_usages,
    collect_event_handler_usages,
    collect_launch_config_usages,
    collect_python_variable_usages,
)
from parser.parser.postprocessing import simplify_launch_configurations
from parser.parser.utils import group_entities_by_type


def parse_and_format_launch_file(filepath: str) -> dict:
    """
    Parses a ROS2 launch file and return output in the standardized grouped format.
    """
    raw = parse_launch_file(filepath)
    grouped = group_entities_by_type(raw["parsed"] + raw["additional_components"])
    
    grouped = collect_composable_node_containers(grouped, raw["composable_containers"])

    launch_argument_usages = collect_launch_config_usages(grouped)
    if launch_argument_usages:
        grouped["launch_argument_usages"] = launch_argument_usages

    undeclared_launch_configurations = raw.get("undeclared_launch_configurations")
    if undeclared_launch_configurations:
        grouped["undeclared_launch_configurations"] = undeclared_launch_configurations

    environment_variables = raw.get("environment_variables")
    if environment_variables:
        grouped["environment_variables"] = environment_variables

    environment_variable_usages = collect_environment_variable_usages(grouped)
    if environment_variable_usages:
        grouped["environment_variable_usages"] = environment_variable_usages

    event_handlers = collect_event_handler_usages(grouped)
    if event_handlers:
        grouped["event_handlers"] = event_handlers

    python_expressions = raw.get("python_expressions")
    if python_expressions:
        grouped["python_expressions"] = raw.get("python_expressions")

    python_expression_usages = collect_python_variable_usages(grouped)
    if python_expression_usages:
        grouped["python_expression_usages"] = python_expression_usages

    return simplify_launch_configurations(grouped)
