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

import re
from collections import defaultdict

from parser.parser.type_mapping import TYPE_KEY_MAP

LAUNCH_CONFIG_REGEX = re.compile(r"\${LaunchConfiguration:([a-zA-Z0-9_]+)}")
ENVIRONMENT_VAR_REGEX = re.compile(r"\${EnvironmentVariable:([a-zA-Z0-9_]+)}")
EVENT_HANDLER_REGEX = re.compile(r"\${EventHandler\[(\d+)\]:(\w+)}")
PYTHON_VAR_REGEX = re.compile(r"\${var:([a-zA-Z_][a-zA-Z0-9_]*)}")


def collect_launch_config_usages(grouped: dict) -> list[dict]:
    """
    Recursively walk the grouped data and return all LaunchConfiguration usages
    with field + JSON-style path, for traceability.
    """
    usages = []

    def walk(obj, path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "type" and obj.get("type") == "LaunchConfiguration":
                    arg = obj.get("name")
                    usages.append({"argument": arg, "path": path})
                else:
                    walk(value, f"{path}.{key}" if path else key)

        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")

        elif isinstance(obj, tuple):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")

        elif isinstance(obj, str):
            for match in LAUNCH_CONFIG_REGEX.finditer(obj):
                usages.append({"argument": match.group(1), "path": path})

    for top_key in TYPE_KEY_MAP.values():
        for idx, entry in enumerate(grouped.get(top_key, [])):
            walk(entry, f"{top_key}[{idx}]")

    return usages


def collect_environment_variable_usages(grouped: dict) -> list[dict]:
    """
    Recursively walk the grouped data and return all EnvironmentVariable usages
    with field + JSON-style path, for traceability.
    """
    usages = []

    def walk(obj, path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "type" and obj.get("type") == "EnvironmentVariable":
                    arg = obj.get("name")
                    usages.append({"argument": arg, "path": path})
                else:
                    walk(value, f"{path}.{key}" if path else key)

        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")

        elif isinstance(obj, tuple):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")

        elif isinstance(obj, str):
            for match in ENVIRONMENT_VAR_REGEX.finditer(obj):
                usages.append({"argument": match.group(1), "path": path})

    for top_key in TYPE_KEY_MAP.values():
        for idx, entry in enumerate(grouped.get(top_key, [])):
            walk(entry, f"{top_key}[{idx}]")

    return usages


def collect_event_handler_usages(grouped: dict) -> list[dict]:
    """
    Recursively walk the grouped data and return all event handler usages
    with index, type and path in the structured output.
    """
    usage_map = defaultdict(lambda: {"type": None, "triggered_by": [], "triggers": []})

    def walk(obj, path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                walk(value, f"{path}.{key}" if path else key)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")
        elif isinstance(obj, tuple):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")
        elif isinstance(obj, str):
            for match in EVENT_HANDLER_REGEX.finditer(obj):
                idx = int(match.group(1))
                handler_type = match.group(2)

                usage_map[idx]["type"] = handler_type

                # Remove trailing index of triggers and triggered_by
                clean_path = path.rsplit("[", 1)[0] if path.endswith("]") else path

                if ".triggers" in clean_path:
                    usage_map[idx]["triggered_by"].append(clean_path)
                elif ".triggered_by" in clean_path:
                    usage_map[idx]["triggers"].append(clean_path)

    for key in TYPE_KEY_MAP.values():
        for idx, item in enumerate(grouped.get(key, [])):
            walk(item, f"{key}[{idx}]")

    return [v for v in usage_map.values() if v["triggered_by"] or v["triggers"]]


def collect_python_variable_usages(grouped: dict) -> list[dict]:
    """
    Recursively walk the grouped data and return all ${var:...} usages
    with variable name + JSON-style path for traceability
    """
    usages = []

    def walk(obj, path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                walk(value, f"{path}.{key}" if path else key)

        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")

        elif isinstance(obj, tuple):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")

        elif isinstance(obj, str):
            for match in PYTHON_VAR_REGEX.finditer(obj):
                usages.append({"variable": match.group(1), "path": path})

    for top_key in TYPE_KEY_MAP.values():
        for idx, entry in enumerate(grouped.get(top_key, [])):
            walk(entry, f"{top_key}[{idx}]")

    return usages

def collect_composable_node_containers(grouped: dict, composable_containers: dict) -> dict:
    """
    Recursively walk the grouped data and return the instances of composable_nodes_container
    """
    def walk(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "composable_nodes_container":
                    containers = obj.get("composable_nodes_container")
                    for idx, container in enumerate(containers):
                        container_name = container.get("target_container")
                        new_container = composable_containers.get(container_name, {})
                        obj[key][idx] = new_container
                else:
                    walk(value)

        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                walk(item)

        elif isinstance(obj, tuple):
            for idx, item in enumerate(obj):
                walk(item)

    walk(grouped)
    return grouped