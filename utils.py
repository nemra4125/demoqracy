from webob.exc import HTTPBadRequest

def ProcessParams(request, optional_params, required_params):
  params = {}

  for required_param in required_params:
    value = request.get(required_param, None)
    if value not in (None, ""):
      params[required_param] = value
    else:
      raise HTTPBadRequest("Required parameter '%s' is missing." %
                           required_param)

  for optional_param in optional_params:
    value = request.get(optional_param, None)
    if value not in (None, ""):
      params[optional_param] = value

  return params