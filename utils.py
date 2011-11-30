from webob.exc import HTTPBadRequest
import hashlib
import simplejson

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
    if len(value) < 2 or value[0] in (None, ""):
      value = value[0]
    if value not in (None, ""):
      params[optional_param] = value

  return params

def WriteJsonResponse(handler, obj):
  handler.response.headers['Content-Type'] = 'application/json'
  handler.response.write(simplejson.dumps(obj))

def MungeEmailToId(user):
  return hashlib.md5(user.email()).hexdigest()