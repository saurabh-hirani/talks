import requests
import base64
import grequests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, ConnectTimeout

# TODO
# - add content-type validation for parallel http
# - find a better way to handle failed urls in parallel call
# - handle greenlet connection failures

class HTTPError(Exception): pass
class HTTPJsonError(HTTPError): pass

DEFAULT_HTTP_TIMEOUT = 60

def do_http_get(url, **kwargs):
  # update default params
  params = {
    'username': None,
    'password': None,
    'timeout': DEFAULT_HTTP_TIMEOUT
  }
  params.update(kwargs)

  # do http get
  try:
    if params['username'] and params['password']:
      response = requests.get(url,
                              timeout=params['timeout'],
                              auth=HTTPBasicAuth(params['username'],
                                                 params['password']))
    else:
      response = requests.get(url, timeout=params['timeout'])
  except (ConnectionError, ConnectTimeout) as e:
    raise HTTPJsonError('%s: connection failed: %s' % (url, e))

  # validate status code
  if response.status_code != 200:
    raise HTTPJsonError('%s: status code - %d' % (url, response.status_code))

  return response

def do_http_get_json(url, **kwargs):
  params = {}
  params.update(kwargs)

  response = do_http_get(url, **params)

  # validate content type
  content_type = response.headers['content-type']
  if response.headers['content-type'] != 'application/json':
    raise HTTPJsonError('%s: Invalid content type - [%s]' % (url,
                                                             content_type))

  return response.json()

def do_parallel_http_get(urls, kwargs):
  # update default params
  params = {
    'timeout': DEFAULT_HTTP_TIMEOUT
  }
  params.update(kwargs)

  headers={}
  if params['username'] and  params['password']:
    authstr = params['username'] + ':' + params['password']
    headers = {'Authorization': 'Basic ' + base64.b64encode(authstr)}

  data = [grequests.get(url, headers=headers,
                        timeout=params['timeout']) for url in urls]

  responses = {}
  valid_urls = []

  for response in grequests.map(data):
    try:
      responses[response.request.url] = response
    except AttributeError as e:
      # hack to handler failed urls
      pass

  return responses
