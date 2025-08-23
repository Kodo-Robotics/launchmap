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

from xml.etree import ElementTree as ET

from parser.context import ParseContext

def strip_ns(tag: str) -> str:
    return tag.split('}')[-1]

def normalize_keys(attrs: dict, key_map: dict) -> dict:
    """
    Normalize XML attribute keys to unified schema keys.
    """
    normalized = {}
    for key, value in attrs.items():
        norm_key = key_map.get(key, key)
        normalized[norm_key] = value
    return normalized

def resolve_parameters(element: ET.Element, context: ParseContext):
    """
    Process the parameter values from given XML tag.
    """
    kwargs = {}
    for key, value in element.attrib.items():
        kwargs[key] = _process_value(value, context)
    
    return kwargs

def resolve_children(element: ET.Element, context: ParseContext):
    """
    Recursively resolve children of a launch XML element.
    Returns a list of accumulated resolved children.
    """
    from parser.parser.xml.dispatcher import dispatch_element

    results = []
    for child in element:
        parsed = dispatch_element(child, context)
        if not parsed:
            continue
        results.append(parsed)

    return results

def _process_value(value: str, context: ParseContext):
    """
    Process an attribute or text value.
    If it contains $(), delegate to substitution handlers.
    Otherwise, return as plain string.
    """
    from parser.parser.xml.dispatcher import dispatch_substitution

    if value is None:
        return None
    value = value.strip()
    if value.startswith("$(") and value.endswith(")"):
        expr = value[2:-1]
        return dispatch_substitution(expr, context)
    return value