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

from parser.parser.type_mapping import TYPE_KEY_MAP


def flatten_once(items):
    """
    Flatten a list one level deep.
    [[a, b], c] -> [a, b, c]
    """
    flattened = []
    for item in items:
        if isinstance(item, list):
            flattened.extend(item)
        else:
            flattened.append(item)
    return flattened


def compute_entity_key(entity: dict) -> str:
    """
    Generate a unique key for deduplication and tracking event links.
    Uses type + package + executable + name if present.
    """
    t = entity.get("type", "")
    pkg = entity.get("package", "")
    exe = entity.get("executable", "")
    name = entity.get("name", "")
    return f"{t}::{pkg}::{exe}::{name}"


def group_entities_by_type(entities: list) -> dict:
    grouped = {}

    for item in entities:
        if not isinstance(item, dict):
            continue
        type_key = item.get("type")
        if not type_key:
            continue

        group_key = TYPE_KEY_MAP.get(type_key)
        if not group_key:
            continue

        clean_item = {k: v for k, v in item.items() if k != "type"}
        grouped.setdefault(group_key, []).append(clean_item)

    return {k: v for k, v in grouped.items() if v}
