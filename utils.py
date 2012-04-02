# Copyright 2012 Google Inc. All Rights Reserved.
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

from webob.exc import HTTPBadRequest
import json

def ProcessParams(request, optional_params, required_params):
  params = {}
  for required_param in required_params:
    value = request.params.getall(required_param)
    if len(value) < 2 or value[0] in (None, ""):
      value = value[0]
    if value not in (None, ""):
      params[required_param] = value
    else:
      raise HTTPBadRequest("Required parameter '%s' is missing." %
                           required_param)
  for optional_param in optional_params:
    value = request.params.getall(optional_param)
    if len(value) < 2 or value[0] in (None, "", "0"):
      value = value[0]
    if value not in (None, "", "0"):
      params[optional_param] = value
  return params

def WriteJsonResponse(handler, obj):
  handler.response.headers['Content-Type'] = 'application/json'
  handler.response.write(json.dumps(obj))