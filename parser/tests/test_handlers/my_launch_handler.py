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
from parser.parser.user_handler import register_user_handler
from parser.resolution.utils import resolve_call_signature

@register_user_handler("MyLaunch")
def handle_my_launch(node, context):
    args, _ = resolve_call_signature(node, context.engine)
    if not args:
        raise ValueError("MyLaunch must have a name.")
    
    name = args[0]

    return simplify_launch_configurations({
        "type": "CustomHandler", 
        "type_name": "MyLaunch",
        "name": name
    })