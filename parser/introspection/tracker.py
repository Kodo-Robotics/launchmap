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

from parser.parser.utils import compute_entity_key


class IntrospectionTracker:
    def __init__(self):
        # All declared arguments from DeclareLaunchArgument
        self.declared_launch_args: dict[str, dict] = {}

        # All names used in LaunchConfiguration(...)
        self.used_launch_configs: set[str] = set()

        # Environment variables
        self.environment_variables: dict[str, dict] = {}

        # Event Handler List
        self.event_handlers: list[str] = []

        # Entity deduplication key -> entity
        self.entities_by_key: dict[str, dict] = {}

        # Python Expressions
        self.symbolic_python_expressions = []

    # Launch Configuration
    def track_launch_arg_declaration(self, name: str, metadata: dict):
        """
        Called by DeclareLaunchArgument handler.
        Stores default_value, description, etc.
        """
        self.declared_launch_args[name] = metadata or {}

    def track_launch_config_usage(self, name: str):
        """
        Called by LaunchConfiguration handler.
        Adds the name to the used set.
        """
        self.used_launch_configs.add(name)

    def get_undeclared_launch_configs(self) -> set[str]:
        """
        Returns all LaunchConfigurations used but not declared.
        Useful for validation and diagnostics.
        """
        return self.used_launch_configs - set(self.declared_launch_args.keys())

    # Environment Variables
    def track_environment_variable(self, name: str, metadata: dict):
        """
        Called by EnvironmentVariable handler.
        Adds the name to the used set.
        """
        self.environment_variables[name] = metadata or {}

    def get_environment_variables(self) -> list:
        """
        Returns all EnvironmentVariable.
        """
        return list(self.environment_variables.values())

    # Event Handler
    def add_event_handler(self, handler: str):
        """
        Registers an event handler
        """
        self.event_handlers.append(handler)

    def next_event_handler_index(self) -> int:
        """
        Return the index of the next event handler
        """
        return len(self.event_handlers)

    def register_entity(self, entity):
        """
        Add entity to output only once (used for nodes, timers, loginfo, etc.)
        """
        key = compute_entity_key(entity)
        if key not in self.entities_by_key:
            self.entities_by_key[key] = entity

    def get_registered_entities(self):
        """
        Get all the registered entities
        """
        return list(self.entities_by_key.values())

    # Python Expressions
    def track_python_expression(self, body: str, variables: list[str]):
        self.symbolic_python_expressions.append({"body": body, "variables": variables})

    def get_python_expressions(self) -> list[dict]:
        return self.symbolic_python_expressions
